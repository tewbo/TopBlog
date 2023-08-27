import bisect
import os
import sys

from PIL import ImageFont, Image

import drawer
import utils
import yandex_cloud as yc
from utils import levenshtein, error

# todo * to png/jpg

PROMPT = "дочитывания\nи просмотры"
MAX_WIDTH = 1500
MAX_HEIGHT = 1500
MIN_WIDTH = 1000
MIN_HEIGHT = 1000


def prepare_int(s):
    return s.replace(" ", "")


def get_center(block):
    (min_x, min_y), (max_x, max_y) = drawer.get_bounds(block)
    return ((min_x + max_x) // 2, (min_y + max_y) // 2)


def show(img, marker_block=None, target_block=None):
    if os.getenv('__DEBUG__'):
        UNICODE_FONT = ImageFont.truetype(
            "JetBrainsMonoNL-SemiBold.ttf", 14)
        if marker_block:
            BOX_STYLE = {"outline": "red", "width": 1}
            drawer.draw_boxes(img, [marker_block], BOX_STYLE, "black", UNICODE_FONT)
        if target_block:
            BOX_STYLE = {"outline": "blue", "width": 1}
            drawer.draw_boxes(img, [target_block], BOX_STYLE, "black", UNICODE_FONT)
        img.show()


def process(imgs, folder_id, iam):
    imgs = [drawer.resize(img, MIN_WIDTH, MIN_HEIGHT, MAX_WIDTH, MAX_HEIGHT) for img in imgs]
    data = []
    for i in range(0, len(imgs), yc.MAX_FILE_COUNT):
        data.extend(yc.parse(imgs[i:i + yc.MAX_FILE_COUNT], folder_id, iam))

    def do(img, blocks):
        ###############
        # FIND MARKER #
        ###############
        sorted_data = sorted(blocks,
                             key=lambda block: (levenshtein(PROMPT, block["text"].lower()), -get_center(block)[1]))
        if not sorted_data:
            show(img)
            error("No markers found on a picture")
            return None
        marker_block = sorted_data[0]

        ###############
        # FIND TARGET #
        ###############

        # todo make it smarter
        # ../zn/images/e1f2662d-a1ee-4653-8a15-a385ba8b5568.png
        def filter_targets(block, marker):
            bounds = drawer.get_bounds(marker)
            return bounds[0][0] <= get_center(block)[0] <= bounds[1][0] and utils.is_number(prepare_int(block['text']))

        # Change blocks with lines
        sorted_data = sorted(blocks, key=lambda b: get_center(b)[1])
        index = bisect.bisect_right(sorted_data, get_center(marker_block)[1], key=lambda b: get_center(b)[1])
        targets = list(filter(lambda b: filter_targets(b, marker_block), sorted_data[index:]))
        if not targets:
            # show(img, marker_block)
            error("No target text found on a picture")
            return None
        target_block = targets[0]

        ##########
        #  DRAW  #
        ##########
        show(img, marker_block, target_block)
        return int(prepare_int(target_block["text"]))

    return list(map(lambda x: do(*x), zip(imgs, data)))


def parse_image(image_path):
    folder_id = os.getenv('YC_FOLDER_ID')
    iam = os.getenv('YC_IAM')
    img = Image.open(image_path)
    return process([img], folder_id, iam)[0]


def do_main(*args):
    # todo make from one to MAX_FILE_COUNT files
    ##############
    #    ARGS    #
    ##############
    if len(args) != 2:
        error("Exactly one parameter expected: file name")
        return None

    file_name = args[1]
    folder_id = os.getenv('YC_FOLDER_ID')
    if not folder_id:
        error("YC_FOLDER_ID variable must be set")
        return None

    iam = os.getenv('YC_IAM')
    if not iam:
        error("YC_IAM variable must be set")
        return None

    ###############
    # OPEN&RESIZE #
    ###############
    file = open(file_name, "rb")
    img = Image.open(file)
    return process([img], folder_id, iam)


def test():
    with open('dzen.test', 'w') as file:
        for filename in os.listdir('images_dzen'):
            try:
                result = do_main('kekw', 'images_dzen/' + filename)
            except Exception as ex:
                print(ex)
                continue
            if result[0]:
                file.write('{:<10}'.format(*result) + '\t' + filename + '\n')
                file.flush()
            else:
                print(filename)


if __name__ == "__main__":
    test()
    # result = do_main(*sys.argv)
    # if result:
    #     print(result)
    #     sys.exit(0)
    # else:
    #     sys.exit(1)

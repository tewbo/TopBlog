import math

from utils import error
import yandex_cloud as yc
from PIL import Image
import os

CHARS_TO_DELETE = [' ']

def get_center(z1, z2):
    (x1, y1) = z1
    (x2, y2) = z2
    return (x1 + x2) // 2, (y1 + y2) // 2


def delete_chars(s: str, chars: list):
    for char in chars:
        s = s.replace(char, '')
    return s


def parse_blocks(blocks):
    data = []
    for block in blocks:
        vertices = block['boundingBox']['vertices']
        try:
            # todo: remove toggle
            cords = (int(vertices[0]['x']), int(vertices[2]['y'])), (int(vertices[0]['x']), int(vertices[2]['y']))
        except:
            data.append(('', ((-1e9, -1e9), (-1e9, -1e9))))
            continue
        words = block['text'].split()
        for word in words:
            data.append((word, cords))
    return data


def parse_image(image_path):
    # Поиск и извлечение текста с изображения
    # result = reader.readtext(image_path)

    folder_id = os.getenv('YC_FOLDER_ID')

    iam = os.getenv('YC_IAM')
    image = Image.open(image_path)

    parsed_blocks = yc.parse([image], folder_id, iam)[0]
    result = parse_blocks(parsed_blocks)

    numbers = []
    err_vr = None
    mobile_case = False
    # todo: try except for cases when result is empty
    for detection in result:
        text = detection[0]
        ((x1, y1), (x2, y2)) = detection[1]
        text = delete_chars(text, CHARS_TO_DELETE).lower()
        if text.replace('%', '').replace('.', '').isdigit():
            numbers.append((text, get_center((x1, y2), (x2, y2))))
        text = text.replace('.', '')
        if err_vr is None and (text == 'err' or text == 'vr'):
            err_vr = get_center((x1, y1), (x2, y2))
        if err_vr is None and text == '(err)':
            err_vr = get_center((x1, y1), (x2, y2))
            mobile_case = True

    if err_vr is None:
        error('Could not find metric')
        return

    dist = 2 ** 32
    final_text = None
    for (text, (x, y)) in numbers:
        if mobile_case and y > err_vr[1]:
            continue
        new_dist = math.hypot(err_vr[0] - x, err_vr[1] - y)
        if new_dist < dist:
            dist = new_dist
            final_text = text

    # print(final_text)
    return final_text
    # log.close()
    # log_numbers.close()


def test():
    with open("tg_test.txt", "w") as file:
        for filename in os.listdir('images_tg'):
            try:
                file.write('{:<10}'.format(parse_image('images_tg/' + filename)) + '\t' + filename + '\n')
                file.flush()
            except Exception as ex:
                print(filename, ex)


def process():
    # filename = "058a18ba-4c82-48fb-bbef-6d33195e4b3f.PNG"
    filename = input("filename: ")
    print(parse_image("images_tg/" + filename))


if __name__ == "__main__":
    # test()
    process()

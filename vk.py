import math

from utils import error
import yandex_cloud as yc
from PIL import Image
import os

CHARS_TO_DELETE = [' ', '~', ',']


def get_center(z1, z2):
    (x1, y1) = z1
    (x2, y2) = z2
    return (x1 + x2) // 2, (y1 + y2) // 2


def delete_chars(s: str, chars: list):
    for char in chars:
        s = s.replace(char, '')
    return s


def find_near(cords, numbers):
    dist = 2 ** 32
    final_text = '0'
    for (text, (x, y)) in numbers:
        new_dist = math.hypot(cords[0] - x, cords[1] - y)
        if new_dist < dist:
            dist = new_dist
            final_text = text
    return int(final_text)


def check_digit(s: str):
    s = delete_chars(s, CHARS_TO_DELETE)
    return s.replace('%', '').replace('.', '').replace('k', '').replace('к', '').isdigit()


def parse_blocks(blocks):
    data = []
    for block in blocks:
        for word_block in block['lines']:
            vertices = word_block['boundingBox']['vertices']
            try:
                cords = (int(vertices[0]['x']), int(vertices[0]['y'])), (int(vertices[2]['x']), int(vertices[2]['y']))
            except:
                data.append(('', ((-1e9, -1e9), (-1e9, -1e9))))
                continue
            words = block['text'].split()
            merged_words = []
            for word in words:
                if len(merged_words) != 0 and check_digit(word) and check_digit(merged_words[-1]):
                    merged_words[-1] += word
                else:
                    merged_words.append(word)

            for word in merged_words:
                data.append((word, cords))
    return data


def parse_image(image_path):
    folder_id = os.getenv('YC_FOLDER_ID')

    iam = os.getenv('YC_IAM')
    image = Image.open(image_path)

    parsed_blocks = yc.parse([image], folder_id, iam)[0]
    result = parse_blocks(parsed_blocks)

    numbers = []
    friends = None
    subscribers = None
    friends_font_size = 0
    # err_vr = None
    # mobile_case = False
    # todo: try except for cases when result is empty
    crop_x = 0
    for detection in result:
        text = delete_chars(detection[0], CHARS_TO_DELETE).lower()
        if text == 'звонки ':
            ((x1, y1), (x2, y2)) = detection[1]
            crop_x = x2

    for detection in result:
        text = detection[0]
        ((x1, y1), (x2, y2)) = detection[1]
        if (x1 + x2) // 2 < crop_x:
            continue
        text = delete_chars(text, CHARS_TO_DELETE).lower()
        if check_digit(text):
            if text[-1] in ["к", 'k']:
                text = str(int(float(text[:-1]) * 1000))
            numbers.append((text, get_center((x1, y2), (x2, y2))))
        text = text.replace('.', '')
        if friends is None and text in ["друг", "друзья", "друга", "друзей"]:
            friends = get_center(*detection[1])
            friends_font_size = abs(y2 - y1)
        if subscribers is None and text in ["участник", "участники", "участника", "участников", "подписчик",
                                            "подписчики",
                                            "подписчика", "подписчиков"]:
            subscribers = get_center(*detection[1])

    if subscribers is None and friends is None:
        error('Could not find metric')
        return

    if subscribers is not None and (friends is None or friends[1] + friends_font_size * 1.5 < subscribers[1] or subscribers[0] <= friends[0]):
        return str(find_near(subscribers, numbers))
    else:
        a1 = 0
        a2 = 0
        if subscribers is not None:
            a1 = find_near(subscribers, numbers)
        if friends is not None:
            a2 = find_near(friends, numbers)
        return str(a1 + a2)


def test():
    with open("vk_test.txt", "w") as file:
        for filename in os.listdir('images_vk'):
            try:
                file.write('{:<10}'.format(parse_image('images_vk/' + filename)) + '\t' + filename + '\n')
                file.flush()
            except Exception as ex:
                print(filename, ex)


def process():
    filename = "0b6be368-ceb4-4702-9509-8ba6d51ab3cf.png"
    # filename = input("filename: ")
    print(parse_image("images_vk/" + filename))


if __name__ == "__main__":
    test()
    # process()

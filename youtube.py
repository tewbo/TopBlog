import os

import easyocr
import numpy as np
from PIL import Image


def ocr(image):
    reader = easyocr.Reader(['ru'])
    results = reader.readtext(np.array(image))
    return results


def to_words(results):
    words_list = [result[1].lower() for result in results]
    if len(words_list) == 1:
        words_list = ' '.join(words_list).split()
    return words_list


def crop_for_subs(image, results):
    target_phrases = ["текущая статистика", "аналитика по каналу", "подписчики", "подписчиков", "подписчик",
                      "подписчика", "число подписчиков"]
    found = False
    for target_phrase in target_phrases:
        for (bbox, text, prob) in results:
            if target_phrase.lower() in text.lower():
                found = True
                x, y = bbox[0][0], bbox[0][1]
                width, height = bbox[2][0] - bbox[0][0], bbox[2][1] - bbox[0][1]
                if target_phrase.lower() in ["текущая статистика", "аналитика по каналу"]:
                    cropped_image = image.crop((x, y, x + width, image.height))
                elif target_phrase.lower() in ["число", "подписчиков"]:
                    cropped_image = image.crop((x, 0, x + width, y + height))
                elif target_phrase.lower() not in ["число подписчиков"] and target_phrase.lower() in ["подписчик",
                                                                                                      "подписчика",
                                                                                                      "подписчиков"]:
                    cropped_image = image.crop((0, y, x + width, y + height))
                else:
                    cropped_image = image.crop((x, 0, x + width, image.height))
                break
        if found:
            break

    if not found:
        cropped_image = image
    return cropped_image


def is_not_counted(words_list):
    if words_list[0] != 'аналитика по каналу' and words_list[0] != 'текущая статистика':
        return True
    return False


def detect_subs(words_list):
    subs = None
    if words_list[0] == 'аналитика по каналу':
        idx = words_list.index('подписчики') + 1
        subs = words_list[idx]

    elif words_list[0] == 'текущая статистика':
        idx = words_list.index('подписчики') - 1
        subs = words_list[idx]

    elif is_not_counted(words_list) and 'подписчики' in words_list:
        idx = words_list.index('подписчики') - 1
        subs = words_list[idx]

    elif 'число подписчиков' in words_list:
        idx = words_list.index('число подписчиков') - 1
        subs = words_list[idx]

    elif 'подписчиков' in words_list:
        idx = words_list.index('подписчиков') - 1
        subs = words_list[idx]

    elif 'подписчика' in words_list:
        idx = words_list.index('подписчика') - 1
        subs = words_list[idx]

    elif 'подписчик' in words_list:
        idx = words_list.index('подписчик') - 1
        subs = words_list[idx]

    return subs


def is_without_views(words):
    if "управление видео" in words or "просмотр" not in ''.join(words):
        return True
    return False


def crop_for_views(image, results):
    target_phrases = ["сводные данные", "статистика по каналу", "просмотров", "за последние 28 дней ваши видео набрали",
                      "в выбранный промежуток времени ваши видео набрали"]
    delete_phrases = ["новости", "идеи для вас"]

    for phrase in delete_phrases:
        for (bbox, text, prob) in results:
            if phrase.lower() in text.lower():
                x, y = bbox[0][0], bbox[0][1]
                image = image.crop((0, 0, x, image.height))

    found = False
    for target_phrase in target_phrases:
        for (bbox, text, prob) in results:
            if target_phrase.lower() in text.lower():
                found = True
                x, y = bbox[0][0], bbox[0][1]
                width, height = bbox[2][0] - bbox[0][0], bbox[2][1] - bbox[0][1]
                if target_phrase.lower() in ["сводные данные"]:

                    cropped_image = image.crop((x, y, image.width, image.height))
                elif target_phrase.lower() in ["статистика по каналу"]:
                    cropped_image = image.crop((x, y, x + width, image.height))
                elif target_phrase.lower() in ["просмотров", "просмотра", "просмотр"]:
                    cropped_image = image.crop((x, 0, x + width, y + height))
                else:
                    cropped_image = image.crop((x, 0, x + width, image.height))
                break
        if found:
            break

    if not found:
        cropped_image = image
    return cropped_image


def detect_views(words_list):
    views = 0
    if words_list[0] == 'сводные данные':
        idx = words_list.index('просмотры') + 1
        views = words_list[idx]

    elif words_list[0] == 'статистика по каналу':
        idx = words_list.index('просмотры') + 1
        views = words_list[idx]

    elif 'просмотров' in words_list:
        idx = words_list.index('просмотров') - 1
        views = words_list[idx]

    elif 'просмотра' in words_list:
        idx = words_list.index('просмотра') - 1
        views = words_list[idx]


    elif 'просмотр' in words_list:
        idx = words_list.index('просмотр') - 1
        views = words_list[idx]

    return views


def parse_image_subscribers(image_path):
    image = Image.open(image_path)
    results = ocr(image)
    word_list = to_words(results)
    img_cropped_s = crop_for_subs(image, results)
    subs = detect_subs(to_words(ocr(img_cropped_s)))
    return subs


def parse_image_views(image_path):
    image = Image.open(image_path)
    results = ocr(image)
    word_list = to_words(results)
    if is_without_views(word_list):
        return None

    img_cropped_v = crop_for_views(image, results)
    views = detect_views(to_words(ocr(img_cropped_v)))
    return views


if __name__ == '__main__':
    path = input('Введите путь к файлу: ')
    image = Image.open(path)
    results = ocr(image)
    word_list = to_words(results)

    img_cropped_s = crop_for_subs(image, results)
    subs = detect_subs(to_words(ocr(img_cropped_s)))
    print(f'Количество подписчиков: {subs}')

    if is_without_views(word_list):
        print('Информация о просмотрах за месяц не предоставлена')
    else:
        img_cropped_v = crop_for_views(image, results)
        views = detect_views(to_words(ocr(img_cropped_v)))
        print(f'Количество просмотров за месяц: {views}')

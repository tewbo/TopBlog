import pandas as pd


def create_table(option):
    df = None
    match option:
        case 'yt1':
            df = pd.DataFrame(columns=['Количество подписчиков', 'image'])
        case 'yt2':
            df = pd.DataFrame(columns=['Просмотры за месяц', 'image'])
        case 'tg':
            df = pd.DataFrame(columns=['VR', 'image'])
        case 'vk':
            df = pd.DataFrame(columns=['Количество подписчиков', 'image'])
        case 'zn':
            df = pd.DataFrame(columns=['Количество дочитываний', 'image'])
    return df


def add_to_table(data, filename, result, option):
    match option:
        case 'tg':
            data = data.append({'VR': result, 'image': filename}, ignore_index=True)
        case 'vk':
            data = data.append({'Количество подписчиков': result, 'image': filename}, ignore_index=True)
        case 'zn':
            data = data.append({'Количество дочитываний': result, 'image': filename}, ignore_index=True)
        case 'yt1':
            data = data.append({'Количество подписчиков': result, 'image': filename}, ignore_index=True)
        case 'yt2':
            data = data.append({'Просмотры за месяц': result, 'image': filename}, ignore_index=True)
    return data


def save_table(data, option):
    match option:
        case 'tg':
            data.to_excel('tg.xlsx', index=False)
        case 'vk':
            data.to_excel('vk.xlsx', index=False)
        case 'zn':
            data.to_excel('zn.xlsx', index=False)
        case 'yt1':
            data.to_excel('yt1.xlsx', index=False)
        case 'yt2':
            data.to_excel('yt2.xlsx', index=False)
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
            data.loc[data.shape[0]] = {'VR': result, 'image': filename}
        case 'vk':
            data.loc[data.shape[0]] = {'Количество подписчиков': result, 'image': filename}
        case 'zn':
            data.loc[data.shape[0]] = {'Количество дочитываний': result, 'image': filename}
        case 'yt1':
            data.loc[data.shape[0]] = {'Количество подписчиков': result, 'image': filename}
        case 'yt2':
            data.loc[data.shape[0]] = {'Просмотры за месяц': result, 'image': filename}
    return data


def save_table(data, option):
    table_name = option + '.xlsx'
    data.to_excel(table_name, index=False)
    return table_name

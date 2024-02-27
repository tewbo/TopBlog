from PIL import Image
import tg
import youtube
import dzen
import vk
import excel
import os
import zipfile
import shutil
import extracter
from datetime import datetime
from get_iam import get_token

last_date = datetime.now()


def parse_single(fp, mode):
    global last_date
    if datetime.now() > last_date:
        resp = get_token()
        os.environ["YC_IAM"] = resp['iamToken']
        last_date = resp['expiresAt']
        print(last_date)
    match mode:
        case 'tg':
            result = tg.parse_image(fp)
        case 'yt1':
            result = youtube.parse_image_subscribers(fp)
        case 'yt2':
            result = youtube.parse_image_views(fp)
        case 'vk':
            result = vk.parse_image(fp)
        case 'zn':
            result = dzen.parse_image(fp)
    return result


def process(file, mode):
    for dirname in ['tmp', 'prepared', 'extracted']:
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
    if file.filename[-3:].lower() == 'zip':
        file.save("tmp/" + file.filename)
        with zipfile.ZipFile("tmp/" + file.filename, 'r') as zip_ref:
            zip_ref.extractall('extracted')
    else:
        file.save("extracted/" + file.filename)

    table = excel.create_table(mode)
    for filename in os.listdir('extracted'):
        try:
            if filename[-3:].lower() == 'pdf':
                extracter.save_pdf_image("extracted/" + filename)
            elif filename[-3:].lower() == 'doc' or filename[-4:].lower() == 'docx':
                extracter.save_doc_image("extracted/" + filename)
            else:
                shutil.move("extracted/" + filename, 'prepared/image1.png')
            fp = 'prepared/image1.png'
            result = parse_single(fp, mode)
            excel.add_to_table(table, filename, result, mode)
        except Exception as e:
            excel.add_to_table(table, filename, '', mode)
            print(filename, e, e.args)
    # excel.add_to_table(table, "filename", result, mode)
    table_name = excel.save_table(table, mode)
    shutil.rmtree('extracted')
    shutil.rmtree('tmp')
    # os.mkdir('tmp')
    shutil.rmtree('prepared')
    # os.mkdir('prepared')
    return table_name


if __name__ == "__main__":
    process("images_tg/0c1986d0-b96f-448f-a59b-e1ae6e34c67e.png", "tg")

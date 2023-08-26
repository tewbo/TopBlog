from PIL import ImageFont, Image

import drawer
import yandex_cloud as yc

FOLDER_ID = "b1g4ju1c9nnua4cubmtg"
IAM = "t1.9euelZrIyZ6YyciJi5WWypeRxouene3rnpWak5THipCNy56enpaWj5XNkcjl9PcPcldY-e9lG2223fT3TyBVWPnvZRttts3n9euelZqTj5SWyZKal5aRnMiZxorKj-_8xeuelZqTj5SWyZKal5aRnMiZxorKjw.-PVhL4bWC5Pv7WfgiHZ3s-qFInHfIwK-hP5Vm6gT2V0niGZbgfnTfjKqIpOiEtOawsrwMAxY5cvMj5ACY8eHBg"
UNICODE_FONT = ImageFont.truetype("JetBrainsMonoNL-SemiBold.ttf", 14)
BLOCK_STYLE = {"outline": "red", "width": 3}
LINE_STYLE = {"outline": "green", "width": 2}
WORD_STYLE = {"outline": "blue", "width": 1}

if __name__ == "__main__":
    n = int(input("Enter number of files: "))
    files = [Image.open(open('images_tg/' + input("Enter file name: ").strip(), "rb")) for _ in range(n)]
    data = yc.parse(files, FOLDER_ID, IAM)
    for i in range(n):
        files[i].seek(0)
        drawer.draw(files[i], data[i], BLOCK_STYLE, LINE_STYLE, WORD_STYLE, "black", UNICODE_FONT)
        files[i].show()

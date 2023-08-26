from pypdf import PdfReader
from utils import error
import docx2txt


def save_pdf_image(filename):
    reader = PdfReader("example.pdf")
    for page in reader.pages:
        for image in page.images:
            with open("prepared/image1.png", "wb") as fp:
                fp.write(image.data)
                return
    error("There is no images in pdf file")


if __name__ == "__main__":
    save_pdf_image("example.pdf")
    # text = docx2txt.process("example.docx", 'prepared/')

from PIL import Image
import sys, fitz
import os
from HelloWorld.settings import * 

"""
pip install PyMuPDF
pip install PIL
"""


def update_image_size(image_name, output_name):
    try:
        img = Image.open("{}{}".format(IMAGE_OUTPUT_PATH, image_name))
        img.resize(COVER_SIZE).save("{}{}".format(IMAGE_OUTPUT_PATH, output_name))
    except Exception as e:
        logging.error("A Book Happen Error When Resize Cover, {}".format(e))
        return False

    return True

def generate_pdf_cover(pdf_name, output_name):
    try:
        pdfDoc = fitz.open("{}{}".format(PDF_INPUT_PATH, pdf_name))
        pdfDoc[0].getPixmap().writePNG("{}{}".format(IMAGE_OUTPUT_PATH, output_name))
    except Exception as e:
        logging.error("A Book Happen Error When Generate Cover, {}".format(e))
        return False
        
    return True

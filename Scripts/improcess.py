from PIL import Image
import sys, fitz
import os

"""
pip install PyMuPDF
pip install PIL
"""
COVER_SIZE = (112, 163)
PDF_INPUT_PATH = "../Statics/bookData/"
OUTPUT_PATH = "../Statics/image/pdf_cover/"


def update_image_size(image_name, output_name):
    img = Image.open("{}{}".format(IMAGE_OUTPUT_PATH, pdf_name))
    img.resize(COVER_SIZE).save("{}{}".format(IMAGE_OUTPUT_PATH, output_name))
    return COVER_SIZE

def generate_pdf_cover(pdf_name, output_name):
    pdfDoc = fitz.open("{}{}".format(PDF_INPUT_PATH, pdf_name))
    pdfDoc[0].getPixmap().writePNG("{}{}".format(IMAGE_OUTPUT_PATH, output_name))
    return output_name

# generate_pdf_cover("C:/Users/vixtel/Downloads/TESTC.pdf")

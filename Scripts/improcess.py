from PIL import Image
import sys, fitz
import os

"""
pip install PyMuPDF
pip install PIL
"""
COVER_SIZE = (112, 163)
PDF_INPUT_PATH = "../Statics/bookData/"
IMAGE_OUTPUT_PATH = "../Statics/image/pdf_cover/"


def update_image_size(image_name, output_name):
    img = Image.open("{}{}".format(IMAGE_OUTPUT_PATH, pdf_name))
    img.resize(COVER_SIZE).save("{}{}".format(IMAGE_OUTPUT_PATH, output_name))
    return COVER_SIZE

def generate_pdf_cover(pdf_name, output_name):
    pdfDoc = fitz.open("{}{}".format(PDF_INPUT_PATH, pdf_name))
    pdfDoc[0].getPixmap().writePNG("{}{}".format(IMAGE_OUTPUT_PATH, output_name))
    return output_name

pdf_path = "Statics/bookData/b-d41d8cd98f00b204e9800998ecf8427e.pdf"
def split_pdf(pdf_path):
    # 先建立PDF文件夹
    dir_name, file_name_with_ext = os.path.split(pdf_path)
    file_name_no_ext, _ = os.path.splitext(file_name_with_ext) 
    file_dir_name = os.path.join(dir_name, file_name_no_ext)

    if os.path.exists(file_dir_name): os.rmdir(file_dir_name)
    os.mkdir(file_dir_name)
    
    with fitz.open(pdf_path) as pdf_pages:
        pages_count = pdf_pages.page_count
        print(pages_count)
        file_num = 0
        page_num = 0
        for page_num in range(100, pages_count, 100):
            pdf = fitz.open()
            pdf.insert_pdf(pdf_pages, from_page=page_num-100, to_page=page_num)
            pdf.save("{}/{:0>2d}.pdf".format(file_dir_name, file_num))
            pdf.close()
            file_num += 1

        if page_num != pages_count:
            pdf = fitz.open()
            pdf.insert_pdf(pdf_pages, from_page=page_num, to_page=pages_count)
            pdf.save("{}/{:0>2d}.pdf".format(file_dir_name, file_num))
            pdf.close()
            

split_pdf(pdf_path)

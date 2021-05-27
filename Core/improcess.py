from PIL import Image
import sys, fitz
import os
import shutil
from HelloWorld.settings import * 
from HelloWorld.settings import logger as log

"""
pip install PyMuPDF
pip install PIL
"""
def generate_pdf_cover(pdf_name, output_name):
    """
    获取PDF文档的第一页作为封面图片
    """
    try:
        log.debug("[ Book Process ] {} Cover Begin To Generate".format(pdf_name))
        pdfDoc = fitz.open("{}{}".format(PDF_INPUT_PATH, pdf_name))
        pdfDoc[0].getPixmap(matrix=fitz.Matrix(16.0, 16.0).preRotate(0), alpha=False).writePNG("{}{}".format(IMAGE_OUTPUT_PATH, output_name))

    except Exception as e:
        log.error("[ Book Process ] A Book Happen Error When Generate Cover, {}".format(e))
        return False

    log.debug("[ Book Process ] {} Cover Generate Success".format(pdf_name))    
    return True

def update_image_size(image_name):
    """
    重新调整图片大小为设置的宽高
    """
    try:
        log.debug("[ Book Process ] {} Image Begin To Update Size".format(image_name))
        img = Image.open("{}{}".format(IMAGE_OUTPUT_PATH, image_name))
        img.resize(COVER_SIZE).save("{}{}".format(IMAGE_OUTPUT_PATH, image_name))

    except Exception as e:
        log.error("[ Book Process ] A Book Happen Error When Resize Cover, {}".format(e))
        return False

    log.debug("[ Book Process ] {} Image Update Size Success".format(image_name))
    return True

def split_pdf(pdf_path):
    """
    对PDF文件进行切割，每100页，切割为一个小PDF 
    """
    log.debug("[ Book Process ] {} Begin To Spilt To Some Pieces".format(pdf_path)) 
    dir_name, file_name_with_ext = os.path.split(pdf_path)
    file_name_no_ext, _ = os.path.splitext(file_name_with_ext) 
    file_dir_name = os.path.join(dir_name, file_name_no_ext)

    if os.path.exists(file_dir_name): shutil.rmtree(file_dir_name)
    os.mkdir(file_dir_name)

    try:
        with fitz.open(pdf_path) as pdf_pages:
            pages_count = pdf_pages.page_count
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
    except:
        log.error("[ Book Process ] A Book Happen Error When Split Pdf, {}".format(e))
        return False

    log.debug("[ Book Process ] {} Spilt To Some Pieces Success".format(pdf_path)) 
    return True

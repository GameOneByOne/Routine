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

pdf_path = "Statics/bookData/b-8c68cc99eab6bfb9c58da2ae96e42a3b.pdf"
def split_pdf(pdf_path):
    # 先建立PDF文件夹
    dir_name, file_name_with_ext = os.path.split(pdf_path)
    file_name_no_ext, _ = os.path.splitext(file_name_with_ext) 
    file_dir_name = os.path.join(dir_name, file_name_no_ext)

    if os.path.exists(file_dir_name): os.rmdir(file_dir_name)
    os.mkdir(file_dir_name)
    
    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc):
            with open("{}/{:0>5d}.txt".format(file_dir_name, page_num), "w", encoding="utf-8") as f:
                f.write(page.getText() + '\n')

    pdf = None
    page_num = 0
    for page_num, txt_file in enumerate(os.listdir(file_dir_name)):
        if (page % 100 == 0):
            if pdf: 
                pdf.save("{}/{:0>5d}.pdf".format(file_dir_name, page_num/100))
                pdf.close()
            pdf = fitz.open()

        with open("{}/{:0>5d}.txt".format(file_dir_name, page_num)) as f:
            pdf.insertPDF()


split_pdf(pdf_path)

from django.apps import AppConfig
from Core import improcess

class BookConfig(AppConfig):
    name = 'HelloWorld.Book'


class ProcessBookQueue:
    def __init__(self):
        pass

    def process(self, item):
        improcess.generate_pdf_cover(item+".pdf", item+".jpeg")
        improcess.update_image_size(item+".jpeg", item+".jpeg")
        improcess.split_pdf("Statics/bookData/{}.pdf".format(item))

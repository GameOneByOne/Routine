from django.apps import AppConfig
from Core import improcess
from Core.processQuque import ProcessQueue
from HelloWorld.Book.models import Book
from HelloWorld.settings import logger as log

class BookConfig(AppConfig):
    name = 'HelloWorld.Book'


class ProcessBookQueue(ProcessQueue):
    def __init__(self, q_name):
        super().__init__(q_name)

    def process(self, item):
        if (improcess.generate_pdf_cover(item+".pdf", item+".jpeg") and \
            improcess.update_image_size(item+".jpeg", item+".jpeg") and \
            improcess.split_pdf("Statics/bookData/{}.pdf".format(item))):
                log.debug("[ ProcessBookQueue ] {} Process Success!".format(item))
                cur_book = Book.objects.get(slug=item)
                cur_book.public = True
                cur_book.update()

        else:
            pass

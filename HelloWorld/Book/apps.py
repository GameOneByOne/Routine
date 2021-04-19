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
        from HelloWorld.ProcessQueue.apps import pQueueManager
        
        book_slug = item[1]
        csrf = item[0]
        if (improcess.generate_pdf_cover(book_slug+".pdf", book_slug+".jpeg") and \
            improcess.update_image_size(book_slug+".jpeg", book_slug+".jpeg") and \
            improcess.split_pdf("Statics/bookData/{}.pdf".format(book_slug))):
                log.debug("[ ProcessBookQueue ] {} Process Success!".format(book_slug))
                cur_book = Book.objects.get(slug=book_slug)
                cur_book.public = True
                cur_book.update()
                
                if csrf != "":
                    pQueueManager.push("RemindMessageQueue", [item[0], "[info]你刚刚上传的 <font color=\"blue\">{}</font> 已经处理完啦，刷新页面即可看到".format(cur_book.name)])
                return 

        if csrf != "":
            pQueueManager.push("RemindMessageQueue", [item[0], "[error]你刚刚上传的 <font color=\"blue\">{}</font> 在处理的时候产生错误，上传失败".format(cur_book.name)])

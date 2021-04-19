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
        
        csrf, book_slug = item[0], item[1]
        if (improcess.generate_pdf_cover("{}.pdf".format(book_slug), "{}.jpeg".format(book_slug)) and \
            improcess.update_image_size("{}.jpeg".format(book_slug)) and \
            improcess.split_pdf("Statics/bookData/{}.pdf".format(book_slug))):
                log.debug("[ ProcessBookQueue ] {} Book Pdf Process Success!".format(book_slug))
                cur_book = Book.objects.get(slug=book_slug)
                cur_book.public = True
                cur_book.update()
                log.debug("[ ProcessBookQueue ] {} Book Data Update Success!".format(book_slug))
                
                pQueueManager.push("RemindMessageQueue", [item[0], "[info]你刚刚上传的 <font color=\"blue\">{}</font> 已经处理完啦，刷新页面即可看到".format(cur_book.name)])
                return 

        log.debug("[ ProcessBookQueue ] {} Book Pdf Process Failed!".format(book_slug))
        pQueueManager.push("RemindMessageQueue", [item[0], "[error]你刚刚上传的 PDF 在处理的时候产生错误，处理失败"])
        return 

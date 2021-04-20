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
        # 将此import放到外面会导致python的引用错误，临时先放在这里
        from HelloWorld.ProcessQueue.apps import pQueueManager
        
        csrf, book_slug = item[0], item[1]
        # if判断中，完成三部分的事情：1.生成PDF封面图片；2.调整封面图片的大小；3.分割PDF文件成小碎片，方便阅读
        if (improcess.generate_pdf_cover("{}.pdf".format(book_slug), "{}.jpeg".format(book_slug)) and \
            improcess.update_image_size("{}.jpeg".format(book_slug)) and \
            improcess.split_pdf("Statics/bookData/{}.pdf".format(book_slug))):
                log.debug("[ ProcessBookQueue ] {} Book Pdf Process Success!".format(book_slug))
                # 这里图书要更新一下public这个字段值，表示可以正常上线显示
                cur_book = Book.objects.get(slug=book_slug)
                cur_book.public = True
                cur_book.save()
                log.debug("[ ProcessBookQueue ] {} Book Data Update Success!".format(book_slug))
                
                # 给用户的消息推送
                pQueueManager.push("RemindMessageQueue", [item[0], "[info]你刚刚上传的 <font color=\"blue\">{}</font> 已经处理完啦，刷新页面即可看到".format(cur_book.name)])
                return 

        log.debug("[ ProcessBookQueue ] {} Book Pdf Process Failed!".format(book_slug))
        pQueueManager.push("RemindMessageQueue", [item[0], "[error]你刚刚上传的 PDF 在处理的时候产生错误，处理失败"])
        return 

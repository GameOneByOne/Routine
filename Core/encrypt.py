import hashlib
import time
from django.utils.text import slugify



def md5(s : str):
    return hashlib.md5(s.encode(encoding='UTF-8')).hexdigest()


def generate_slug(type : str):
    pass
    # if type == ""
    # elif type ==
    # else:
    #     return 
    # return slugify("1 2312 1513 61 234")
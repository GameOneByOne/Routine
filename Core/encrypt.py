import hashlib
import time
from django.utils.text import slugify



def md5(s: str):
    """
    返回字符类型的MD5
    """
    return hashlib.md5(s.encode(encoding='UTF-8')).hexdigest()


def generate_slug(type: str, key: str):
    """
    返回一个唯一的MD5标识
    """
    if type == "Stock":
        return slugify("S {}".format(md5(key)))
    
    if type == "User":
        return slugify("U {}".format(md5(key)))

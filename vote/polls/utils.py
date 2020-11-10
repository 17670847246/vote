import random

ALL_CHARS ='1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'

def random_captcha(length=4):
    return ''.join(random.choices(ALL_CHARS, k=length))



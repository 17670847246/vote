import hashlib
import random
import re

import requests

ALL_CHARS ='1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'

def random_captcha(length=4):
    return ''.join(random.choices(ALL_CHARS, k=length))

def to_md5_hex(content):
    return hashlib.md5(content.encode()).hexdigest()


def random_mobile_code(length=6):
    return ''.join(random.choices('1234567890', k=length))

def send_message_by_sms(*, tel, message):
    resp = requests.post(
        url='http://sms-api.luosimao.com/v1/send.json',
        auth=('api', 'bbfb1c5649f4a735e5d10ecdc46b4e5e'),
        data={
            'mobile': tel,
            'message': message
        }, timeout=3, verify=False)
    return resp.json()


USERNAME_PATTERN = re.compile(r'[0-9a-zA-Z_]{6,20}')
TEL_PATTERN = re.compile(r'1[3-9]\d{9}')

def check_username(username):
    """检查用户名"""
    return USERNAME_PATTERN.fullmatch(username) is not None

def check_password(password):
    """检查密码"""
    return len(password) >= 8

def check_tel(tel):
    """检查手机号"""
    return TEL_PATTERN.fullmatch(tel) is not None





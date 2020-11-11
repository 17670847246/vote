import json

from django.db import DatabaseError
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from polls.captcha import Captcha
from polls.models import Subject, Teachers, User
from polls.utils import random_captcha, to_md5_hex, send_message_by_sms, random_mobile_code, check_username, \
    check_password, check_tel


def show_subject(request: HttpRequest) -> HttpResponse:
    subject = Subject.objects.all()
    return render(request, 'subjects.html', {'subjects': subject})


def show_teachers(request: HttpRequest) -> HttpResponse:
    try:
        sno = int(request.GET['sno'])
        subject = Subject.objects.get(no=sno)
        queryset = Teachers.objects.filter(subject__no=sno)
        return render(request, 'teachers.html', {
            'teachers': queryset,
            'subject': subject,
        })
    except (KeyError, ValueError, Subject.DoesNotExist):
        return redirect('/')


def praise_or_ratings(request: HttpRequest) -> HttpResponse:
    """好评"""
    if request.session.get('userid'):
        try:
            tno = request.GET['tno']
            teacher = Teachers.objects.get(no=tno)
            if request.path == '/praise/':
                teacher.good_count += 1
                count = teacher.good_count
            else:
                teacher.bad_count += 1
                count = teacher.bad_count
            teacher.save()
            data = {'code': 10000, 'message': '投票成功', 'count': count}
        except (KeyError, ValueError, Teachers.DoesNotExist):
            data = {'code': 10001, 'message': '投票失败'}
    else:
        data = {'code': 10002, 'message': '请先登录再投票'}
    return JsonResponse(data)


def get_captcha(request: HttpRequest) -> HttpResponse:
    """生成验证码图片"""
    code = random_captcha()
    request.session['captcha'] = code
    image_data = Captcha.instance().generate(code)
    return HttpResponse(image_data, content_type='image/png')


def login(request: HttpRequest) -> HttpResponse:
    """登入"""
    hint = ''
    backurl = request.GET.get('backurl', '/')
    if request.method == 'POST':
        backurl = request.POST.get('backurl', '/')
        code_from_user = request.POST.get('captcha', '0')
        code_from_sess = request.session.get('captcha', '1')
        if code_from_sess.lower() == code_from_user.lower():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            if check_username(username) and check_password(password):
                password = to_md5_hex(password)
                user = User.objects\
                    .filter(Q(username=username) | Q(tel=username))\
                    .filter(password=password).first()
                if user:
                    request.session['userid'] = user.no
                    request.session['username'] = user.username
                    return redirect(backurl)
                else:
                    hint = '用户名或密码错误'
            else:
                hint = '请输入有效的用户名和密码'
        else:
            hint = '请输入正确的验证码'
    return render(request, 'login.html', {'hint': hint, 'backurl':backurl})

def logout(request: HttpRequest) -> HttpResponse:
    """注销"""
    request.session.flush()
    return redirect('/login/')

def register(request: HttpRequest) -> HttpResponse:
    """注册"""
    hint = ''
    if request.method == 'POST':
        agreement = request.POST.get('agreement')
        if agreement == 'on':
            code_from_user = request.POST.get('mobilecode', '0')
            code_from_sess = request.session.get('mobilecode', '1')
            if code_from_user == code_from_sess:
                username = request.POST.get('username')
                password = request.POST.get('password')
                password = to_md5_hex(password)
                tel = request.POST.get('tel')
                if check_username(username) and check_password(password)\
                        and check_tel(tel):
                    user = User()
                    user.username = username
                    user.password = password
                    user.tel = tel
                    try:
                        user.save()
                    except DatabaseError:
                        hint = '用户名或手机号已被注册，请尝试其他的用户名或手机号'
                    else:
                        hint = '注册成功，请登录'
                        return redirect(f'/login/?hint={hint}')
                else:
                    hint = '请输入有效的注册信息'
            else:
                hint = '请输入有效的验证码'
        else:
            hint = '请勾选同意网站用户协议及隐私政策'
    return render(request, 'register.html', {'hint': hint})


def send_mobile_code(request: HttpRequest, tel) -> HttpResponse:
    """发送验证码"""
    code = random_mobile_code()
    request.session['mobilecode'] = code
    message = f'您的短信验证码为{code}, 【铁壳测试】'
    send_message_by_sms(tel=tel, message=message)
    return JsonResponse({'code': 20000, 'message': '短信验证码已经发送到您的手机'})



def is_unique_username(request: HttpRequest) -> HttpResponse:
    """检查用户唯一性"""
    username = request.GET.get('username')
    if check_username(username):
        if User.objects.filter(username=username).exists():
            data = {'code': 30001, 'message': '用户已被注册'}
        else:
            data = {'code': 30000, 'message': '用户名可以使用'}
    else:
        data = {'code': 30002, 'message': '无效的用户名'}
    return JsonResponse(data)
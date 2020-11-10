import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from polls.captcha import Captcha
from polls.models import Subject, Teachers, User
from polls.utils import random_captcha, to_md5_hex


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
    code = random_captcha()
    image_data = Captcha.instance().generate(code)
    return HttpResponse(image_data, content_type='image/png')


def login(request: HttpRequest) -> HttpResponse:
    """登入"""
    # request.path / request.method / request.is_ajax()
    # request.GET / request.POST / request.FILES / request.META / request.COOKIES
    # request.data / request.get_full_path() / request.issecure()
    hint = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username and password:
            password = to_md5_hex(password)
            user = User.objects.filter(username=username, password=password).first()
            if user:
                request.session['userid'] = user.no
                request.session['username'] = user.username
                return redirect('/')
            else:
                hint = '用户名或密码错误'
        else:
            hint = '请输入有效的用户名和密码'
    return render(request, 'login.html', {'hint': hint})

def logout(request: HttpRequest) -> HttpResponse:
    """注销"""
    request.session.flush()
    return redirect('/login/')

def register(request: HttpRequest) -> HttpResponse:
    return render(request, 'register.html')

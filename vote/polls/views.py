import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from polls.captcha import Captcha
from polls.models import Subject, Teachers
from polls.utils import random_captcha


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
    return JsonResponse(data)


def get_captcha(request: HttpRequest) -> HttpResponse:
    code = random_captcha()
    image_data = Captcha.instance().generate(code)
    return HttpResponse(image_data, content_type='image/png')


def login(request: HttpRequest) -> HttpResponse:
    return render(request, 'login.html')


def register(request: HttpRequest) -> HttpResponse:
    return render(request, 'register.html')

import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from polls.models import Subject, Teachers


def show_subject(request: HttpRequest) -> HttpResponse:
    subject = Subject.objects.all()
    return render(request, 'subjects.html', {'subjects':subject})


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
            teacher.bad_count +=1
            count = teacher.bad_count
        teacher.save()
        data = {'code': 10000, 'message': '投票成功', 'count':count}
    except (KeyError, ValueError, Teachers.DoesNotExist):
        data = {'code': 10001, 'message': '投票失败'}
    return JsonResponse(data)

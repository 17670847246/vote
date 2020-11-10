from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from polls.models import Subject, Teachers


def show_subject(request: HttpRequest) -> HttpResponse:
    subject = Subject.objects.all()
    return render(request, 'subjects.html', {'subjects':subject})


def show_teachers(request: HttpRequest) -> HttpResponse:
    try:
        sno = int(request.GET.get('sno', ''))
        queryset = Teachers.objects.filter(subject__no=sno)
        return render(request, 'teachers.html', {'teachers': queryset})
    except (KeyError, ValueError):
        return redirect('/')
from django.http import HttpRequest, HttpResponse
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



def praise(request: HttpRequest) -> HttpResponse:
    """好评"""
    sno = request.GET.get('sno', '0')
    try:
        tno = request.GET['tno']
        teacher = Teachers.objects.get(no=tno)
        teacher.good_count += 1
        teacher.save()
    except (KeyError, ValueError, Teachers.DoesNotExist):
        pass
    return redirect(f'/teachers/?sno={sno}')

def ratings(request: HttpRequest) -> HttpResponse:
    """差评"""
    sno = request.GET.get('sno', '0')
    try:
        tno = request.GET['tno']
        teacher = Teachers.objects.get(no=tno)
        teacher.bad_count += 1
        teacher.save()
    except (KeyError, ValueError, Teachers.DoesNotExist):
        pass
    return redirect(f'/teachers/?sno={sno}')
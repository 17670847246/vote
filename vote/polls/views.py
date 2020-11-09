from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
from polls.models import Subject


def show_subject(request: HttpRequest) -> HttpResponse:
    subject = Subject.objects.all()
    return render(request, 'subjects.html', {'subjects':subject})
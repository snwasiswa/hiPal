from django.shortcuts import render, HttpResponse
from languages.models import Lesson, Language, Content, Module


# Create your views here.

def home(request):
    #return HttpResponse("This is my homepage(/)")
    return render(request,'home.html')

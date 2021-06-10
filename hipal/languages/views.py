from django.shortcuts import render, HttpResponse
from languages.models import Language, Lesson, Module, Content

# Create your views here.

def homepage(request):
    #return HttpResponse("This is my homepage(/)")
    return render(request,'homepage.html')

from django.shortcuts import render, HttpResponse
from .models import Language, Lesson, Module, Content
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView


# Create your views here.
class LessonListView(ListView):
    """View for the list of lessons"""
    model = Lesson
    template_name = 'languages/manage/lesson/list.html'

    def get_queryset(self):
        """Allows to only display or update the lesson created"""
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


def homepage(request):
    #return HttpResponse("This is my homepage(/)")
    return render(request, 'homepage.html')


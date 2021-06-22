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
        return queryset.filter(owner=self.request.creator)


class CreatorMixin(object):
    def get_queryset(self):
        """Allows to only display or update the lesson created"""
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.creator)


class EditableCreatorMixin(object):
    def validate(self, form):
        form.instance.owner = self.request.creator
        return super().validate(form)


class CreatorLessonMixin(CreatorMixin):
    model = Lesson
    fields = ['slug', 'title', 'overview', 'language']
    success_url = reverse_lazy('manage_lesson')


class EditableCreatorMixinLesson(CreatorLessonMixin, EditableCreatorMixin):
    template_name = 'languages/manage/lesson/list.html'


class ManageLessonView(CreatorLessonMixin, ListView):
    template_name = 'languages/manage/lesson/list'


class LessonCreateView(EditableCreatorMixinLesson, CreateView):
    pass


class LessonUpdateView(EditableCreatorMixinLesson, UpdateView):
    pass


class LessonDeleteView(CreatorLessonMixin, DeleteView):
    template_name = 'languages/manage/lesson/delete_lesson.list'


def homepage(request):
    # return HttpResponse("This is my homepage(/)")
    return render(request, 'homepage.html')

from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .forms import StudentEnrollment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from languages.models import Lesson
from django.views.generic.detail import DetailView


# Create your views here.

class RegistrationCreationView(CreateView):
    """A registration view for students that inherits from CreateView"""
    template_name = 'registration/register.html'
    form_class = UserCreationForm

    # success_url = reverse_lazy(students_lessons_list)

    def form_valid(self, form):
        """A form to valid students credentials"""
        result = super().form_valid(form)
        credentials = form.cleaned_data
        login(self.request, authenticate(password=credentials['password'], username=credentials['username']))
        return result


class StudentEnrollmentView(LoginRequiredMixin, FormView):
    """ View of student enrollment lessons which inherits from the LoginRequiredMixin and FormView"""
    lesson = None
    form_class = StudentEnrollment

    def form_valid(self, form):
        """Validation of the form for the lesson"""
        self.lesson = form.cleaned_data['lesson']
        self.lesson.student.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        """ Returns the URL that the user will be directed to if the form is successful"""
        return reverse_lazy('lesson_detail', args=[self.lesson.id])


class StudentLessonView(LoginRequiredMixin, ListView):
    """ View of lessons that students are enrolled on"""
    model = Lesson
    template_name = 'lessons/list_lessons.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(student__in=[self.request.user])


class StudentLessonDetailView(DetailView):
    """ View for student lesson details"""
    model = Lesson
    template_name = 'lessons/details.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(student__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get lesson object
        lesson = self.get_object()
        args = self.kwargs
        # store lesson units
        units = lesson.units
        if 'unit_id' in args:
            # current unit
            context['unit'] = units.get(id=args['unit_id'])
        else:
            # first unit
            context['unit'] = units.all()[0]

        return context


from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .forms import StudentEnrollment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView


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




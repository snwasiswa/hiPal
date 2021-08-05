from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .forms import StudentEnrollment, StudentLoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from languages.models import Lesson
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import StudentRegistrationForm


# Create your views here.
def student_login_view(request):
    """ Login View for Instructors"""
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            credentials = form.cleaned_data
            user = authenticate(request, password=credentials['password'], username=credentials['username'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('student_lesson_list')

                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = StudentLoginForm()
    return render(request, 'languages/templates/account/login.html', {'form': form})


class RegistrationCreationView(CreateView):
    """A registration view for students that inherits from CreateView"""
    template_name = 'registration/instructor_registration.html'
    form_class = UserCreationForm

    success_url = reverse_lazy('student_lesson_list')

    def form_valid(self, form):
        """A form to valid students credentials"""
        result = super().form_valid(form)
        credentials = form.cleaned_data
        login(self.request, authenticate(password=credentials['password'], username=credentials['username']))
        return result


def register(request):
    if request.method == 'POST':

        student_form = StudentRegistrationForm(request.POST)

        if student_form.is_valid():

            new_student = student_form.save(commit=False)
            new_student.set_password(student_form.cleaned_data['password1'])
            new_student.save()

            return HttpResponseRedirect(reverse_lazy('student_lesson_list'))

            # return render(request, 'registration/instructor_registration.html', {'new_student': new_student})
    else:
        student_form = StudentRegistrationForm()
    return render(request, 'registration/register.html', {'student_form': student_form})


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
        return reverse_lazy('student_lesson_details', args=[self.lesson.id])


class StudentLessonView(LoginRequiredMixin, ListView):
    """ View of lessons that students are enrolled on"""
    model = Lesson
    template_name = 'lessons/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(student__in=[self.request.user])


class StudentLessonDetailView(DetailView):
    """ View for student lesson details"""
    model = Lesson
    template_name = 'lessons/student_lesson_detail.html'

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

        return context


class StudentLogin(LoginView):
    """ Student Login View which inherits from LoginView"""

    template_name = 'registration/studentlogin.html'




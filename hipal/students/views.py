from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

# Create your views here.
class RegistrationCreationView(CreateView):
    """A registration view for students"""
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    #success_url = reverse_lazy(students_lessons_list)

    def form_valid(self, form):
        """A form to valid students credentials"""
        result = super().form_valid(form)
        credentials = form.cleaned_data
        login(self.request, authenticate(password=credentials['password'], username=credentials['username']))
        return result



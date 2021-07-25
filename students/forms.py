from django import forms
from languages.models import Lesson
from django.contrib.auth.forms import User


class StudentEnrollment(forms.Form):
    """Form for the student enrollment"""
    lesson = forms.ModelChoiceField(queryset=Lesson.objects.all(), widget=forms.HiddenInput)


class StudentLoginForm(forms.Form):
    """Login form to use for authentication"""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class StudentRegistrationForm(forms.ModelForm):
    """ Student Registration Form"""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password(self):
        credentials = self.cleaned_data
        if credentials['password'] != credentials['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return credentials['password2']

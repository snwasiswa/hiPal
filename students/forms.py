from django import forms
from languages.models import Lesson
from django.contrib.auth.forms import User
from django.utils.translation import gettext, gettext_lazy as _


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

    error_messages = {
        'password_mismatch': _("Sorry! The passwords you entered don't match."),
    }

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

        return password2

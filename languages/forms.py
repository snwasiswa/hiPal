from django import forms
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from .models import Unit, Lesson, Profile
from django.utils.translation import gettext, gettext_lazy as _

UnitFormSet = inlineformset_factory(Lesson,
                                    Unit,
                                    fields=['title', 'description'],
                                    extra=2,
                                    can_order=True,
                                    can_delete=True)


class InstructorLoginForm(forms.Form):
    """Login form to use for authentication"""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class InstructorRegistrationForm(forms.ModelForm):
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


class UserForm(forms.ModelForm):
    """User form to allow users to manage their profiles"""

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class UserProfileForm(forms.ModelForm):
    """User form to allow users to manage their profiles, including their profile photo"""

    class Meta:
        model = Profile
        fields = ('photo',)

from django import forms
from languages.models import Lesson


class StudentEnrollment(forms.Form):
    """Form for the student enrollment"""
    lesson = forms.ModelChoiceField(queryset=Lesson.objects.all(), widget=forms.HiddenInput)


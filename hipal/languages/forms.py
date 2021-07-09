from django import forms
from django.forms.models import inlineformset_factory
from .models import Unit, Lesson

UnitFormSet = inlineformset_factory(Lesson,
                                    Unit,
                                    fields=['title', 'description'],
                                    extra=2,
                                    can_order=True,
                                    can_delete=True)

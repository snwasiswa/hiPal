from django.test import TestCase
from django.test import Client
from .models import Language
from .restapi.serializers import LanguageSerializer


# Create your tests here.
#
# class LanguageSerializerTestCase(TestCase):
# """ Tests for the language serializer"""

class CreateMixinViewTests(TestCase):
    def created_lessons(self):
        pass

    def no_created_lessons(self):
        pass

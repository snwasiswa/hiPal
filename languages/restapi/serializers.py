from ..models import Language, Lesson, Unit
from rest_framework import serializers


class LanguageSerializer(serializers.ModelSerializer):
    """ Provides serializations for model instances"""
    class Meta:
        model = Language
        fields = ['id', 'title', 'slug']


class UnitSerializer(serializers.ModelSerializer):
    """ Provides serializations for model instances"""
    class Meta:
        model = Unit
        fields = ['description', 'title', 'order']


class LessonSerializer(serializers.ModelSerializer):
    """ Provides serializations for model instances"""
    units = UnitSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'slug', 'outline', 'language', 'created_on', 'creator', 'units']


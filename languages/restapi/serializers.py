from abc import ABC

from ..models import Language, Lesson, Unit, Content
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


class ItemSerializer(serializers.RelatedField, ABC):
    """ Provides serializations for model instances"""

    def to_representation(self, value):
        return value.render()


class ContentSerializer(serializers.ModelSerializer):
    """ Provides serializations for model instances"""
    item = ItemSerializer(read_only=True)

    class Meta:
        model = Unit
        fields = ['item', 'order']


class UnitContentSerializer(serializers.ModelSerializer):
    """ Provides serializations for model instances"""
    content = ContentSerializer(many=True)

    class Meta:
        model = Unit
        fields = ['description', 'title', 'order', 'content']


class LessonContentSerializer(serializers.ModelSerializer):
    """ Provides serializations for model instances"""
    units = UnitContentSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ['created_on', 'title', 'slug', 'units', 'id', 'outline', 'creator', 'language']
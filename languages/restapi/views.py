from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LanguageSerializer
from ..models import Language, Lesson
from django.shortcuts import get_object_or_404


class LanguageListView(generics.ListAPIView):
    """ List of languages"""
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class LanguageDetailView(generics.RetrieveAPIView):
    """ Details of languages"""
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class LessonEnrollmentView(APIView):
    """ Lessons Enrollment View"""

    def post(self, request, lesson_id, format=None):
        """Execute post requests"""
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        lesson.student.add(request.user)
        return Response({'enrolled': True})

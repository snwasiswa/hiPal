from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import LanguageSerializer, LessonSerializer
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
        authentication_classes = BasicAuthentication
        permission_classes = IsAuthenticated

        return Response({'enrolled': True})


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    """ ViewSet for the lesson model"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

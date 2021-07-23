from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .serializers import LanguageSerializer, LessonSerializer, LessonContentSerializer
from ..models import Language, Lesson
from django.shortcuts import get_object_or_404
from .permissions import IsRegistered


class LanguageListView(generics.ListAPIView):
    """ List of languages"""
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class LanguageDetailView(generics.RetrieveAPIView):
    """ Details of languages"""
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


"""class LessonRegistrationView(APIView):


    def post(self, request, lesson_id, format=None):
 
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        lesson.student.add(request.user)
        authentication_classes = BasicAuthentication
        permission_classes = IsAuthenticated

        return Response({'Registered': True})"""


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    """ ViewSet for the lesson model"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    @action(detail=True,
            methods=['POST'],
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def register(self, request, *args, **kwargs):
        """Helps for students registration"""
        lesson = self.get_object()
        lesson.student.add(request.user)

        return Response({'Registered': True})

    @action(detail=True,
            methods=['GET'],
            serializer_class=LessonContentSerializer,
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated, IsRegistered])
    def get_content(self, request, *args, **kwargs):
        """Helps to retrieve Lesson object"""
        return self.retrieve(request, *args, **kwargs)

from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import GenericViewSet

class AnswerQuestionView(CreateAPIView, GenericViewSet):
    pass

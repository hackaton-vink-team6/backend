from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Answer, Question
from .serializers import QuestionSerializers


class AnswerQuestionView(CreateAPIView, GenericViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializers
    permission_classes = [permissions.AllowAny, ]

    def create(self, request, *args, **kwargs):
        data = request.data
        #context = generate_questions(data['types'], data['questions'])
        #return Response(context, status=status.HTTP_201_CREATED, )
        pass


from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (AnswerQuestionView)

app_name = 'api'
router_v1 = DefaultRouter()
router_v1.register(r'answer_question', AnswerQuestionView, basename='answers')


urlpatterns = [
    path(r'', include(router_v1.urls)),
]
from rest_framework import serializers
from .models import Answer, Question
#from bot.validators import validate_is_profane_russian


class QuestionSerializers(serializers.ModelSerializer):


    class Meta:
        model = Question
        fields = [
            'profile',
            'text_question',
            'created_at',
        ]

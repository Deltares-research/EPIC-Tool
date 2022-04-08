from __future__ import annotations

from typing import Dict, OrderedDict

from rest_framework import serializers

from epic_app.models.epic_questions import (
    Answer,
    EvolutionQuestion,
    LinkagesQuestion,
    NationalFrameworkQuestion,
    Question,
)
from epic_app.models.models import EpicUser


class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for 'Question'
    """

    class Meta:
        """
        Overriden meta class for serializing purposes.
        """

        model = Question
        fields = "__all__"


class NationalFrameworkQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NationalFrameworkQuestion
        fields = "__all__"


class EvolutionQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvolutionQuestion
        fields = "__all__"


class LinkagesQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkagesQuestion
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    """
    Serializer for 'QuestionAnswerForm'
    """

    class Meta:
        """
        Overriden meta class for serializing purposes.
        """

        model = Answer
        fields = ("url", "id", "user", "question", "short_answer", "long_answer")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def get_user_query_set():
            current_user = self.context["request"].user
            if current_user.is_staff or current_user.is_superuser:
                return EpicUser.objects.all()
            else:
                return EpicUser.objects.all().filter(id=current_user.id)

        self.fields["user"] = serializers.PrimaryKeyRelatedField(
            queryset=get_user_query_set()
        )

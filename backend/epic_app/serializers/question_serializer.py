from __future__ import annotations

from typing import Type

from rest_framework import serializers

from epic_app.models.epic_questions import (
    EvolutionQuestion,
    KeyAgencyActionsQuestion,
    LinkagesQuestion,
    NationalFrameworkQuestion,
    Question,
)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"

    @staticmethod
    def get_concrete_serializer(q_type: Type[Question]) -> serializers.ModelSerializer:
        dict_serializers = {
            NationalFrameworkQuestion: NationalFrameworkQuestionSerializer,
            KeyAgencyActionsQuestion: KeyAgencyQuestionSerializer,
            EvolutionQuestion: EvolutionQuestionSerializer,
            LinkagesQuestion: LinkagesQuestionSerializer,
        }
        serializer = dict_serializers.get(q_type, None)
        if not serializer:
            raise ValueError(f"Question type {q_type} has no designated serializer.")
        return serializer


class NationalFrameworkQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NationalFrameworkQuestion
        fields = "__all__"


class KeyAgencyQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyAgencyActionsQuestion
        fields = "__all__"


class EvolutionQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvolutionQuestion
        fields = "__all__"


class LinkagesQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkagesQuestion
        fields = "__all__"

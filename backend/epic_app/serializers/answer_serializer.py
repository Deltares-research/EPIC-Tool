from typing import Type

from rest_framework import serializers

from epic_app.models.epic_answers import (
    Answer,
    MultipleChoiceAnswer,
    SingleChoiceAnswer,
    YesNoAnswer,
    YesNoAnswerType,
)
from epic_app.models.epic_questions import EvolutionChoiceType


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("url", "id", "user", "question")

    @staticmethod
    def get_concrete_serializer(q_type: Type[Answer]) -> serializers.ModelSerializer:
        dict_serializers = {
            YesNoAnswer: YesNoAnswerSerializer,
            SingleChoiceAnswer: SingleChoiceAnswerSerializer,
            MultipleChoiceAnswer: MultipleChoiceAnswerSerializer,
        }
        serializer = dict_serializers.get(q_type, None)
        if not serializer:
            raise ValueError(f"Question type {q_type} has no designated serializer.")
        return serializer


class YesNoAnswerSerializer(serializers.ModelSerializer):
    short_answer = serializers.ChoiceField(YesNoAnswerType.choices)

    class Meta:
        model = YesNoAnswer
        fields = "__all__"


class SingleChoiceAnswerSerializer(serializers.ModelSerializer):
    selected_choice = serializers.ChoiceField(EvolutionChoiceType.choices)

    class Meta:
        model = SingleChoiceAnswer
        fields = "__all__"


class MultipleChoiceAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleChoiceAnswer
        fields = "__all__"

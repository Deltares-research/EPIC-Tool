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
from epic_app.utils import get_instance_as_submodel_type


class _BaseAnswerSerializer(serializers.ModelSerializer):
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

    def update(self, instance: Answer, validated_data):
        """
        Override of the update method to allow getting the `Answer` subtype instance and prevent from getting constraint errors.
        """
        subtype_instance = get_instance_as_submodel_type(instance)
        return super().update(subtype_instance, validated_data)


class AnswerSerializer(_BaseAnswerSerializer):
    class Meta:
        model = Answer
        fields = ("url", "id", "user", "question")


class YesNoAnswerSerializer(_BaseAnswerSerializer):
    short_answer = serializers.ChoiceField(YesNoAnswerType.choices)

    class Meta:
        model = YesNoAnswer
        fields = "__all__"


class SingleChoiceAnswerSerializer(_BaseAnswerSerializer):
    selected_choice = serializers.ChoiceField(EvolutionChoiceType.choices)

    class Meta:
        model = SingleChoiceAnswer
        fields = "__all__"


class MultipleChoiceAnswerSerializer(_BaseAnswerSerializer):
    # selected_programs = SimpleProgramSerializer(many=True)

    class Meta:
        model = MultipleChoiceAnswer
        fields = "__all__"

    def update(self, instance: Answer, validated_data):
        return super().update(instance, validated_data)

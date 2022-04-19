from rest_framework import serializers

from epic_app.models.epic_answers import (
    Answer,
    MultipleChoiceAnswer,
    SingleChoiceAnswer,
    YesNoAnswer,
)
from epic_app.models.epic_user import EpicUser


class YesNoAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = YesNoAnswer
        fields = ("url", "id", "user", "question", "short_answer", "justify_answer")


class SingleChoiceAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingleChoiceAnswer
        fields = ("url", "id", "user", "question", "selected_choice", "justify_answer")


class MultipleChoiceAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleChoiceAnswer
        fields = (
            "url",
            "id",
            "user",
            "question",
            "selected_programs",
        )

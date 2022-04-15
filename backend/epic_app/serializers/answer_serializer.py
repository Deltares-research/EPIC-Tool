from rest_framework import serializers

from epic_app.models.epic_questions import (
    Answer,
    MultipleChoiceAnswer,
    SingleChoiceAnswer,
    YesNoAnswer,
)
from epic_app.models.epic_user import EpicUser


class YesNoAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = YesNoAnswer
        fields = ("short_answer", "justify_answer")


class SingleChoiceAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingleChoiceAnswer
        fields = ("selected_choice", "justify_answer")


class MultipleChoiceAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleChoiceAnswer
        fields = ("selected_programs",)


class AnswerSerializer(serializers.ModelSerializer):
    """
    Serializer for 'QuestionAnswerForm'
    """

    yesnoanswer = YesNoAnswerSerializer(read_only=True)
    singlechoiceanswer = SingleChoiceAnswerSerializer(read_only=True)
    multiplechoiceanswer = MultipleChoiceAnswerSerializer(read_only=True)

    class Meta:
        """
        Overriden meta class for serializing purposes.
        """

        model = Answer
        fields = (
            "url",
            "id",
            "user",
            "question",
            "yesnoanswer",
            "singlechoiceanswer",
            "multiplechoiceanswer",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def get_user_query_set():
            current_user: EpicUser = self.context["request"].user
            if current_user.is_staff or current_user.is_superuser:
                return EpicUser.objects.all()
            else:
                return EpicUser.objects.all().filter(id=current_user.id)

        self.fields["user"] = serializers.PrimaryKeyRelatedField(
            queryset=get_user_query_set()
        )

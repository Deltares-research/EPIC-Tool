from rest_framework import serializers

from epic_app.models.epic_questions import Answer, Question
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
        fields = ("url", "id", "description", "program")


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

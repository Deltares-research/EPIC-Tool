from rest_framework import serializers

from epic_app.models.models import Program
from epic_app.serializers.question_serializer import QuestionSerializer


class ProgramSerializer(serializers.ModelSerializer):
    """
    Serializer for 'Program'
    """

    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        """
        Overriden meta class for serializing purposes.
        """

        model = Program
        fields = ("url", "id", "name", "description", "agencies", "group", "questions")


class SimpleProgramSerializer(serializers.ModelSerializer):
    """
    Serializer for 'Program' without embedded questions.
    """

    class Meta:
        """
        Overriden meta class for serializing purposes.
        """

        model = Program
        fields = ("url", "id", "name", "description")

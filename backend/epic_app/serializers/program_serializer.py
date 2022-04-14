from rest_framework import serializers

from epic_app.models.models import Program
from epic_app.serializers.question_serializer import (
    EvolutionQuestionSerializer,
    LinkagesQuestionSerializer,
    NationalFrameworkQuestionSerializer,
)


class ProgramSerializer(serializers.ModelSerializer):
    """
    Serializer for 'Program'
    """

    nationalframeworkquestions = NationalFrameworkQuestionSerializer(
        many=True, read_only=True
    )
    evolutionquestions = EvolutionQuestionSerializer(many=True, read_only=True)
    linkagesquestions = LinkagesQuestionSerializer(many=True, read_only=True)

    class Meta:
        """
        Overriden meta class for serializing purposes.
        """

        model = Program
        fields = (
            "url",
            "id",
            "name",
            "description",
            "agencies",
            "group",
            "nationalframeworkquestions",
            "evolutionquestions",
            "linkagesquestions",
        )


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

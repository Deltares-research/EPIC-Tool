from __future__ import annotations

from rest_framework import serializers

from epic_app.models.epic_questions import (
    EvolutionQuestion,
    LinkagesQuestion,
    NationalFrameworkQuestion,
    Question,
)


class NationalFrameworkQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NationalFrameworkQuestion
        fields = "__all__"


class EvolutionQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvolutionQuestion
        fields = (
            "nascent_description",
            "engaged_description",
            "capable_description",
            "effective_description",
        )


class LinkagesQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkagesQuestion
        fields = "__all__"

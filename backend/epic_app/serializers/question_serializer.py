from __future__ import annotations

from rest_framework import serializers

from epic_app.models.epic_questions import (
    EvolutionQuestion,
    KeyAgencyActionsQuestion,
    LinkagesQuestion,
    NationalFrameworkQuestion,
)


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

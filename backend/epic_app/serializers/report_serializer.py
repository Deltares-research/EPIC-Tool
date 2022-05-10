from __future__ import annotations

from typing import Any, Dict, List, Type, Union

from django.db import models
from rest_framework import serializers

from epic_app.models.epic_answers import Answer
from epic_app.models.epic_questions import Question
from epic_app.models.models import Program
from epic_app.serializers.answer_serializer import AnswerSerializer
from epic_app.utils import get_instance_as_submodel_type


class AnswerListReportSerializer(serializers.ListSerializer):
    def _get_answers_summary(
        self, answers_list: Union[models.QuerySet, List[Answer]]
    ) -> Dict[str, Any]:
        if not answers_list or len(answers_list) == 0:
            return {}
        subtype: Type[Answer] = type(
            get_instance_as_submodel_type(answers_list.first())
        )
        subtype_answer_list = subtype.objects.filter(
            id__in=[al.id for al in answers_list]
        )
        return subtype.get_detailed_summary(subtype_answer_list)

    def to_representation(self, data):
        organization_users = self.context["users"].all()
        user_ids = [eu.id for eu in organization_users]
        filtered_data = Answer.objects.filter(question=data.instance, user__in=user_ids)
        answers_summary = self._get_answers_summary(filtered_data)

        serialized_answers = super(AnswerListReportSerializer, self).to_representation(
            filtered_data
        )
        return {"answers": serialized_answers, "summary": answers_summary}


class AnswerReportSerializer(serializers.BaseSerializer):
    class Meta:
        model = Answer
        fields = "__all__"
        list_serializer_class = AnswerListReportSerializer

    def to_representation(self, instance: Answer):
        st_answer: Answer = get_instance_as_submodel_type(instance)
        st_serializer: serializers.ModelSerializer = (
            AnswerSerializer.get_concrete_serializer(type(st_answer))
        )
        return st_serializer(context={"request": self.context}).to_representation(
            st_answer
        )


class QuestionReportSerializer(serializers.ModelSerializer):
    question_answers = AnswerReportSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ("url", "id", "title", "question_answers")


class ProgramReportSerializer(serializers.ModelSerializer):

    questions = QuestionReportSerializer(many=True, read_only=True)

    class Meta:
        model = Program
        fields = ("url", "id", "name", "questions")

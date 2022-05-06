from typing import List, Optional, Tuple

from rest_framework import serializers

from epic_app.models.epic_answers import Answer
from epic_app.models.epic_questions import Question
from epic_app.models.epic_user import EpicUser
from epic_app.models.models import Program
from epic_app.utils import get_instance_as_submodel_type

QuestionAnswer = Tuple[Question, Optional[Answer]]


class QuestionAnswerSerializer(serializers.BaseSerializer):
    def to_representation(self, instance: QuestionAnswer):
        question, answer = instance
        return {question.id: answer.id if answer else None}


class ProgressSerializer(serializers.BaseSerializer):
    def _get_question_answer(self, question: Question) -> QuestionAnswer:
        progress_user: EpicUser = self.context["request"].user
        answer = None
        try:
            answer = Answer.objects.get(user=progress_user, question=question)
            answer = get_instance_as_submodel_type(answer)
        finally:
            return (question, answer)

    def _get_total_progress(self, answer_list: List[QuestionAnswer]) -> float:
        valid_answers = sum(a.valid_answer() for _, a in answer_list if a)
        return valid_answers / len(answer_list)

    def to_representation(self, instance: Program):
        if not isinstance(instance, Program):
            raise ValueError(
                f"Expected instance type {type(Program)}, got {type(instance)}"
            )
        question_answers = [
            self._get_question_answer(q) for q in instance.questions.all()
        ]
        return {
            "progress": self._get_total_progress(question_answers),
            "question_answers": [
                QuestionAnswerSerializer().to_representation(qa)
                for qa in question_answers
            ],
        }

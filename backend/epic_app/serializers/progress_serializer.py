from typing import List, Optional, Tuple

from rest_framework import serializers

from epic_app.models.epic_answers import Answer
from epic_app.models.epic_questions import Question
from epic_app.models.epic_user import EpicUser
from epic_app.models.models import Program
from epic_app.utils import get_instance_as_submodel_type

_QuestionAnswer = Tuple[Question, Optional[Answer]]


class _QuestionAnswerSerializer(serializers.BaseSerializer):
    def to_representation(self, instance: _QuestionAnswer):
        question, answer = instance
        if not isinstance(question, Question):
            raise ValueError("No valid question provided.")
        return {question.id: answer.id if answer else None}


class ProgressSerializer(serializers.BaseSerializer):
    """
    Serializer to show the progress of the context `EpicUser`.
    Only meant for GET / FETCH endpoints.
    """

    def _get_context_epic_user(self) -> EpicUser:
        try:
            return self.context["request"].user
        except:
            raise ValueError("No user found in context-request.")

    def _get_question_answer(self, question: Question) -> _QuestionAnswer:
        progress_user: EpicUser = self._get_context_epic_user()
        answer = None
        try:
            answer = Answer.objects.get(user=progress_user, question=question)
            answer = get_instance_as_submodel_type(answer)
        finally:
            return (question, answer)

    def _get_total_progress(self, answer_list: List[_QuestionAnswer]) -> float:
        valid_answers = sum(a.is_valid_answer() for _, a in answer_list if a)
        return valid_answers / len(answer_list)

    def to_representation(self, instance: Program):
        if not isinstance(instance, Program):
            raise ValueError(
                f"Expected instance type {type(Program)}, got {type(instance)}"
            )
        qa_list = [self._get_question_answer(q) for q in instance.questions.all()]
        qa_dict = {}
        for qa in qa_list:
            qa_dict.update(_QuestionAnswerSerializer().to_representation(qa))
        return {
            "progress": self._get_total_progress(qa_list),
            "questions_answers": qa_dict,
        }

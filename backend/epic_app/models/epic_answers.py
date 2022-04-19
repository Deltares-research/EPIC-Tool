from __future__ import annotations

import abc

from django.db import IntegrityError, models

from epic_app.models import models as base_models
from epic_app.models.epic_questions import EvolutionChoiceType, Question
from epic_app.models.epic_user import EpicUser


class YesNoAnswerType(models.TextChoices):
    YES = "Y"
    NO = "N"


# region Cross-Reference Tables
class Answer(models.Model):
    """
    Cross reference table to define the bounding relationship between a User and the answers they give to each question.

    Args:
        models (models.Model): Derives directly from base class Model.
    """

    user = models.ForeignKey(
        to=EpicUser, on_delete=models.CASCADE, related_name="user_answers"
    )
    question = models.ForeignKey(
        to=Question, on_delete=models.CASCADE, related_name="question_answers"
    )

    class Meta:
        unique_together = ["user", "question"]

    def __str__(self) -> str:
        return f"[{self.user}] {self.question}"


class YesNoAnswer(Answer):
    short_answer: str = models.CharField(
        YesNoAnswerType.choices, max_length=50, blank=True
    )
    justify_answer: str = models.TextField(blank=True)


class SingleChoiceAnswer(Answer):
    selected_choice: str = models.CharField(
        EvolutionChoiceType.choices, max_length=50, blank=True
    )
    justify_answer: str = models.TextField(blank=True)

    def get_selected_choice_text(self) -> str:
        return next(
            c_field
            for c_field in self._meta.get_fields()
            if c_field.verbose_name.lower() == self.selected_choice.lower()
        )


class MultipleChoiceAnswer(Answer):
    selected_programs = models.ManyToManyField(
        to=base_models.Program, blank=True, related_name="selected_answers"
    )


# endregion

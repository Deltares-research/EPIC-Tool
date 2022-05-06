from __future__ import annotations

import abc
from typing import List

from django.db import IntegrityError, models

from epic_app.models import models as base_models
from epic_app.models.epic_questions import (
    EvolutionChoiceType,
    EvolutionQuestion,
    KeyAgencyActionsQuestion,
    LinkagesQuestion,
    NationalFrameworkQuestion,
    Question,
)
from epic_app.models.epic_user import EpicUser


class YesNoAnswerType(models.TextChoices):
    YES = "Y", ("Yes")
    NO = "N", ("No")


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

    def _check_question_integrity(self) -> bool:
        """
        Auxiliar method to be defined in concrete classes which verify the assigned `question` is suitable for this `answer`.
        Base class `Answer` should not support any `Question`.
        Returns:
            bool: Whether the given `Question` type can be assigned to this `Answer` type.
        """
        return any(
            [
                sq.objects.filter(id=self.question.id).exists()
                for sq in self._get_supported_questions()
            ]
        )

    @staticmethod
    def _get_supported_questions() -> List[Question]:
        """
        Method to be overriden in concrete classes. Base `Answer` does not support any `Question`.

        Returns:
            List[Question]: List of supported `Questions`.
        """
        return []

    def save(self, *args, **kwargs) -> None:
        """
        Overriding of the save method to ensure only supported questions are assigned to related answers.
        This is just a way to preserve the question as a base field property to answer without explicitely defining its concrete question.

        Raises:
            IntegrityError: When the `question` field is not supported for this `answer` subtype.
        """
        if not self._check_question_integrity():
            raise IntegrityError(
                "Question type `{}` not allowed. Supported types: [{}].".format(
                    type(self.question).__name__,
                    ", ".join(
                        [f"`{sq.__name__}`" for sq in self._get_supported_questions()]
                    ),
                )
            )

        return super(Answer, self).save(*args, **kwargs)


class YesNoAnswer(Answer):
    short_answer: str = models.CharField(
        YesNoAnswerType.choices, max_length=50, blank=True
    )
    justify_answer: str = models.TextField(blank=True)

    @staticmethod
    def _get_supported_questions() -> List[Question]:
        return [NationalFrameworkQuestion, KeyAgencyActionsQuestion]


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

    @staticmethod
    def _get_supported_questions() -> List[Question]:
        return [EvolutionQuestion]


class MultipleChoiceAnswer(Answer):
    selected_programs = models.ManyToManyField(
        to=base_models.Program, blank=True, related_name="selected_answers"
    )

    @staticmethod
    def _get_supported_questions() -> List[Question]:
        return [LinkagesQuestion]


# endregion

from __future__ import annotations

import abc

from django.db import models

from epic_app.models import models as base_models


class Question(models.Model):

    title: str = models.CharField(null=False, blank=False, max_length=150)
    program: base_models.Program = models.ForeignKey(
        to=base_models.Program, on_delete=models.CASCADE, related_name="questions"
    )

    class Meta:
        unique_together = ["title", "program"]

    def __str__(self) -> str:
        return self.title[0:15]

    @abc.abstractmethod
    def get_answer(self):
        raise NotImplementedError


class NationalFrameworkQuestion(Question):
    description: str = models.TextField(null=False, blank=False)


class EvolutionChoiceType(models.TextChoices):
    NASCENT = "Nascent"
    ENGAGED = "Engaged"
    CAPABLE = "Capable"
    EFFECTIVE = "Effective"


class EvolutionQuestion(Question):
    # Single choice among four options
    nascent_description: str = models.TextField(
        null=False, blank=False, verbose_name=str(EvolutionChoiceType.NASCENT)
    )
    engaged_description: str = models.TextField(
        null=False, blank=False, verbose_name=str(EvolutionChoiceType.ENGAGED)
    )
    capable_description: str = models.TextField(
        null=False, blank=False, verbose_name=str(EvolutionChoiceType.CAPABLE)
    )
    effective_description: str = models.TextField(
        null=False, blank=False, verbose_name=str(EvolutionChoiceType.EFFECTIVE)
    )


class LinkagesQuestion(Question):
    # Up to 3 choices among all available programs in epic domain.
    pass


# region Cross-Reference Tables
class Answer(models.Model):
    """
    Cross reference table to define the bounding relationship between a User and the answers they give to each question.

    Args:
        models (models.Model): Derives directly from base class Model.
    """

    user = models.ForeignKey(
        to=base_models.EpicUser, on_delete=models.CASCADE, related_name="user_answers"
    )
    question = models.ForeignKey(
        to=Question, on_delete=models.CASCADE, related_name="question_answers"
    )

    class YesNoAnswerType(models.TextChoices):
        """
        Defines the Yes / No answer types.

        Args:
            models (models.TextChocies): Derives directly from the base class TextChoices.
        """

        YES = "Y"
        NO = "N"

    short_answer: str = models.CharField(
        YesNoAnswerType.choices, max_length=50, blank=True
    )
    long_answer: str = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"[{self.user}] {self.question}: {self.short_answer}"


# endregion

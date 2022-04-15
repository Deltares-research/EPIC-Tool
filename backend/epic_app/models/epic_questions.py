from __future__ import annotations

import abc

from django.db import IntegrityError, models

from epic_app.models import models as base_models
from epic_app.models.epic_user import EpicUser


class Question(models.Model):

    title: str = models.CharField(null=False, blank=False, max_length=150)
    program: base_models.Program = models.ForeignKey(
        to=base_models.Program, on_delete=models.CASCADE, related_name="questions"
    )

    # class Meta:
    #     unique_together = ["title", "program"]

    def __str__(self) -> str:
        return self.title[0:15]

    @abc.abstractmethod
    def get_answer(self, q_user: EpicUser) -> Answer:
        raise NotImplementedError


class NationalFrameworkQuestion(Question):
    """
    Question of type Yes / No and Justify.
    """

    description: str = models.TextField(null=False, blank=False)

    def get_answer(self, q_user: EpicUser) -> YesNoAnswer:
        if not YesNoAnswer.objects.filter(user=q_user, question=self).exists():
            return YesNoAnswer.objects.create(user=q_user, question=self)
        return YesNoAnswer.objects.filter(user=q_user, question=self).first()


class YesNoAnswerType(models.TextChoices):
    YES = "Y"
    NO = "N"


class EvolutionChoiceType(models.TextChoices):
    NASCENT = "Nascent"
    ENGAGED = "Engaged"
    CAPABLE = "Capable"
    EFFECTIVE = "Effective"


class EvolutionQuestion(Question):
    """
    Question of type 'pick one' between four categories and Justify.
    """

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

    def get_answer(self, q_user: EpicUser) -> SingleChoiceAnswer:
        if not SingleChoiceAnswer.objects.filter(user=q_user, question=self).exists():
            return SingleChoiceAnswer.objects.create(user=q_user, question=self)
        return SingleChoiceAnswer.objects.filter(user=q_user, question=self).first()


class LinkagesQuestion(Question):
    """
    Question of multiple (max 3) choices between all programs registered in the database.
    """

    _linkages_title = "Please select three programs that will help you deliver better results in your program if you could have better collaboration? "

    def save(self, *args, **kwargs) -> None:
        """
        Overriding the default save method to inject a 'fake' OneToOne constraint on the 'program' field.

        Raises:
            IntegrityError: When there's already a LinkagesQuestion for the same program.
        """
        # In theory this could be done with the OneToOne relationship. However I'm unable to override that field or the Meta class.
        if LinkagesQuestion.objects.filter(program=self.program).exists():
            raise IntegrityError(
                "UNIQUE constraint failed: epic_app_question.program_id"
            )
        return super().save(*args, **kwargs)

    def get_answer(self, q_user: EpicUser) -> MultipleChoiceAnswer:
        if not MultipleChoiceAnswer.objects.filter(user=q_user, question=self).exists():
            return MultipleChoiceAnswer.objects.create(user=q_user, question=self)
        return MultipleChoiceAnswer.objects.filter(user=q_user, question=self).first()

    @staticmethod
    def generate_linkages():
        """
        Generates linkages questions for all the available programs
        """
        for p_obj in base_models.Program.objects.all():
            LinkagesQuestion(
                title=LinkagesQuestion._linkages_title, program=p_obj
            ).save()


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

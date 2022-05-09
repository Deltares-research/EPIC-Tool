from __future__ import annotations

from django.db import IntegrityError, models
from django.utils.translation import gettext_lazy as _

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


class YesNoQuestion(Question):
    description: str = models.TextField(null=False, blank=False)

    class Meta:
        abstract = True
        # Override the unique_together clause.
        unique_together = []


class NationalFrameworkQuestion(YesNoQuestion):
    """
    Question of type Yes / No and Justify.
    """

    pass


class KeyAgencyActionsQuestion(YesNoQuestion):
    """
    Question of type Yes / No and Justify.
    """

    pass


class EvolutionChoiceType(models.TextChoices):
    NASCENT = "NASCENT", _("Nascent")
    ENGAGED = "ENGAGED", _("Engaged")
    CAPABLE = "CAPABLE", _("Capable")
    EFFECTIVE = "EFFECTIVE", _("Effective")


class EvolutionQuestion(Question):
    """
    Question of type 'pick one' between four categories and Justify.
    """

    # Single choice among four options
    nascent_description: str = models.TextField(
        null=True, blank=True, verbose_name=str(EvolutionChoiceType.NASCENT)
    )
    engaged_description: str = models.TextField(
        null=True, blank=True, verbose_name=str(EvolutionChoiceType.ENGAGED)
    )
    capable_description: str = models.TextField(
        null=True, blank=True, verbose_name=str(EvolutionChoiceType.CAPABLE)
    )
    effective_description: str = models.TextField(
        null=True, blank=True, verbose_name=str(EvolutionChoiceType.EFFECTIVE)
    )


class LinkagesQuestion(Question):
    """
    Question of multiple (max 3) choices between all programs registered in the database.
    """

    _linkages_title = "Please select three programs that will help you deliver better results in your program if you could have better collaboration? "

    def __str__(self) -> str:
        return f"Linkages for: {self.program}"

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
        return super(LinkagesQuestion, self).save(*args, **kwargs)

    @staticmethod
    def generate_linkages():
        """
        Generates linkages questions for all the available programs
        """
        for p_obj in base_models.Program.objects.all():
            LinkagesQuestion(
                title=LinkagesQuestion._linkages_title, program=p_obj
            ).save()

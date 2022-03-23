from __future__ import annotations
from typing import List
from django.db import models
from django.contrib.auth.models import User

# region Default models
class EpicUser(User):
    """
    Defines the properties for a typical user in EpicTool.

    Args:
        User (auth.models.User): Derives directly from the base class User.
    """
    organization: str = models.CharField(max_length=50)

class Area(models.Model):
    """
    Higher up entity containing a set of Groups.

    Args:
        models (models.Model): Derives directly from the base class Model.
    """
    name: str = models.CharField(max_length=50)

    def get_groups(self) -> List[Group]:
        """
        Gets a list of groups whose area is the caller.

        Returns:
            List[Group]: List of groups frot this area.
        """
        return Group.objects.filter(area=self).all()

class Group(models.Model):
    """
    Higher up entity containing one or programs.

    Args:
        models (models.Model): Derives directly from the base class Model.
    """
    name: str = models.CharField(max_length=50)
    area: Area = models.ForeignKey(
        to=Area,
        on_delete=models.CASCADE,
        related_name='group_area',
        unique=True)
    
    def get_programs(self) -> List[Program]:
        """
        Gets a list of programs whose groups is the caller.

        Returns:
            List[Program]: List of programs for this group.
        """
        return Program.objects.filter(group=self).all()

class Program(models.Model):
    """
    Higher up entity containing one or many questions and answers.

    Args:
        models (models.Model): Derives directly from the base class Model.
    """
    name: str = models.CharField(max_length=50)
    group: Group = models.ForeignKey(
        to=Group,
        on_delete=models.CASCADE,
        related_name='program_group',
        unique=True)

    def get_questions(self) -> List[Question]:
        """
        Gets a list of questions whose program is the caller.

        Returns:
            List[Question]: List of questions for this program.
        """
        return Question.objects.filter(program=self).all()

class Question(models.Model):
    """
    Defines what fields a 'question' entity has.

    Args:
        models (models.Model): Derives directly derived from base class Model.
    """
    description: str = models.TextField(blank=False)
    program: Program = models.ForeignKey(
        to=Program,
        on_delete=models.CASCADE,
        related_name='question_program',
        unique=True)

    def __str__(self) -> str:
        # Show the first 15 chars as a description.
        return self.description[0:15]
# endregion

# region Cross-Reference Tables
class Answer(models.Model):
    """
    Cross reference table to define the bounding relationship between a User and the answers they give to each question.

    Args:
        models (models.Model): Derives directly from base class Model.
    """
    user = models.ForeignKey(
        to=EpicUser,
        on_delete=models.CASCADE,
        related_name='user_answers'
    )
    question = models.ForeignKey(
        to=Question,
        on_delete=models.CASCADE,
        related_name='question_answers'
    )
    
    class YesNoAnswerType(models.TextChoices):
        """
        Defines the Yes / No answer types.

        Args:
            models (models.TextChocies): Derives directly from the base class TextChoices.
        """
        YES = 'Y'
        NO = 'N'

    short_answer: str = models.CharField(YesNoAnswerType.choices, max_length=50, blank=True)
    long_answer: str = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"[{self.user}] {self.question}: {self.short_answer}"

# endregion
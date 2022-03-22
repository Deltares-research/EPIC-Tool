from django.db import models
from django.contrib.auth.models import User

#region Default models
class EpicUser(User):
    """
    Defines the properties for a typical user in EpicTool.

    Args:
        User (auth.models.User): Derives directly from the base class User.
    """
    organization: str = models.CharField(max_length=50)

class Question(models.Model):
    """
    Defines what fields a 'question' entity has.

    Args:
        models (models.Model): Derives directly derived from base class Model.
    """
    description: str = models.TextField(blank=False)
    def __str__(self) -> str:
        # Show the first 15 chars as a description.
        return self.description[0:15]

class Program(models.Model):
    """
    Higher up entity containing one or many questions and answers.

    Args:
        models (models.Model): Derives directly from the base class Model.
    """
    name: str = models.CharField(max_length=50)

class Group(models.Model):
    """
    Higher up entity containing one or more subprograms.

    Args:
        models (models.Model): Derives directly from the base class Model.
    """
    name: str = models.CharField(max_length=50)

class Area(models.Model):
    """
    Higher up entity containing a set of Groups.

    Args:
        models (models.Model): Derives directly from the base class Model.
    """
    name: str = models.CharField(max_length=50)
#endregion

#region Cross-Reference Tables
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

#endregion
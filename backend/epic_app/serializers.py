from rest_framework import serializers

from epic_app.models import EpicUser, UserQuestionAnswers, QuestionAnswerForm, Question, Answer

class EpicUserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for 'EpicUser'
    """
    class Meta:
        """
        Overriden meta class for serializing purposes.
        """
        model=EpicUser
        fields = ('username', 'organization')

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for 'Question'
    """
    class Meta:
        """
        Overriden meta class for serializing purposes.
        """
        model=Question
        fields = ('description')
    
class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for 'Answer'
    """
    class Meta:
        """
        Overriden meta class for serializing purposes.
        """
        model=Answer
        fields = ('short_answer', 'long_answer')

class QuestionAnswerFormSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for 'QuestionAnswerForm'
    """
    class Meta:
        """
        Overriden meta class for serializing purposes.
        """
        model=QuestionAnswerForm
        fields = ('user', 'qa_form')

class UserQuestionAnswersSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for 'UserQuestionAnswers'
    """
    class Meta:
        """
        Overriden meta class for serializing purposes.
        """
        model=UserQuestionAnswers
        fields = ('user', 'qa_form')
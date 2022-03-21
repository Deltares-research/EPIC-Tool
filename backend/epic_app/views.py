# Create your views here.
from rest_framework import viewsets

from epic_app.serializers import EpicUserSerializer, QuestionSerializer, AnswerSerializer, QuestionAnswerFormSerializer, UserQuestionAnswersSerializer
from epic_app.models import EpicUser, UserQuestionAnswers, QuestionAnswerForm, Question, Answer


class EpicUserViewSet(viewsets.ModelViewSet):
    """
    Default view set for 'EpicUser'

    Args:
        viewsets (ModelViewSet): Derives directly from ModelViewSet
    """
    queryset = EpicUser.objects.all().order_by('username')
    serializer_class = EpicUserSerializer

# class QuestionViewSet(viewsets.ModelViewSet):
#     """
#     Default view set for 'Question'

#     Args:
#         viewsets (ModelViewSet): Derives directly from ModelViewSet
#     """
#     queryset = Question.objects.all().order_by('description')
#     serializer_class = QuestionSerializer

# class AnswerViewSet(viewsets.ModelViewSet):
#     """
#     Default view set for 'Answer'

#     Args:
#         viewsets (ModelViewSet): Derives directly from ModelViewSet
#     """
#     queryset = Answer.objects.all().order_by('short_answer')
#     serializer_class = AnswerSerializer

# class QuestionAnswerFormViewSet(viewsets.ModelViewSet):
#     """
#     Default view set for 'QuestionAnswerForm'

#     Args:
#         viewsets (ModelViewSet): Derives directly from ModelViewSet
#     """
#     queryset = QuestionAnswerForm.objects.all().order_by('question')
#     serializer_class = QuestionAnswerFormSerializer

# class UserQuestionAnswersViewSet(viewsets.ModelViewSet):
#     """
#     Default view set for 'UserQuestionAnswers'

#     Args:
#         viewsets (ModelViewSet): Derives directly from ModelViewSet
#     """
#     queryset = UserQuestionAnswers.objects.all().order_by('user')
#     serializer_class = UserQuestionAnswersSerializer
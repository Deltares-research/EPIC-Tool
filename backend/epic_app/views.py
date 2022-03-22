# Create your views here.
from rest_framework import viewsets

from epic_app.serializers import EpicUserSerializer, QuestionSerializer, AnswerSerializer
from epic_app.models import EpicUser, Question, Answer
from rest_framework.views import APIView
from rest_framework.response import Response

# class EpicUserViewSet(APIView):
#     """
#     Default view set for 'EpicUser'

#     Args:
#         viewsets (ModelViewSet): Derives directly from ModelViewSet
#     """
#     # auth_classes = [SessionAuthent]
#     queryset = EpicUser.objects.all().order_by('username')
#     serializer_class = EpicUserSerializer

class EpicUserViewSet(viewsets.ModelViewSet):
    """
    Default view set for 'EpicUser'

    Args:
        viewsets (ModelViewSet): Derives directly from ModelViewSet
    """
    queryset = EpicUser.objects.all().order_by('username')
    serializer_class = EpicUserSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    """
    Default view set for 'Question'

    Args:
        viewsets (ModelViewSet): Derives directly from ModelViewSet
    """
    queryset = Question.objects.all().order_by('description')
    serializer_class = QuestionSerializer

class AnswerViewSet(viewsets.ModelViewSet):
    """
    Default view set for 'Answer'

    Args:
        viewsets (ModelViewSet): Derives directly from ModelViewSet
    """
    queryset = Answer.objects.all().order_by('user')
    serializer_class = AnswerSerializer
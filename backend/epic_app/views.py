# Create your views here.
from rest_framework import viewsets, permissions

from epic_app.serializers import EpicUserSerializer, QuestionSerializer, AnswerSerializer
from epic_app.models import EpicUser, Question, Answer

class EpicUserViewSet(viewsets.ModelViewSet):
    """
    Default view set for 'EpicUser'

    Args:
        viewsets (ModelViewSet): Derives directly from ModelViewSet
    """
    queryset = EpicUser.objects.all().order_by('username')
    serializer_class = EpicUserSerializer
    permission_classes = [permissions.IsAuthenticated]

class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Default view set for 'Question'

    Args:
        viewsets (ModelViewSet): Derives directly from ModelViewSet
    """
    queryset = Question.objects.all().order_by('description')
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

class AnswerViewSet(viewsets.ModelViewSet):
    """
    Default view set for 'Answer'

    Args:
        viewsets (ModelViewSet): Derives directly from ModelViewSet
    """
    queryset = Answer.objects.all().order_by('user')
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

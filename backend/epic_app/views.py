# Create your views here.
from rest_framework import permissions, viewsets

from epic_app.models.models import Agency, Answer, Area, EpicUser, Group, Program, Question
from epic_app.serializers import (
    AgencySerializer,
    AnswerSerializer,
    AreaSerializer,
    EpicUserSerializer,
    GroupSerializer,
    ProgramSerializer,
    QuestionSerializer,
)


class EpicUserViewSet(viewsets.ModelViewSet):
    """
    Default view set for 'EpicUser'

    Args:
        viewsets (ModelViewSet): Derives directly from ModelViewSet
    """

    queryset = EpicUser.objects.all().order_by("username")
    serializer_class = EpicUserSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class AreaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Default view set for 'Area'

    Args:
        viewsets (ModelViewSet): Derives directly from ModelViewSet
    """

    queryset = Area.objects.all().order_by("name")
    serializer_class = AreaSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class AgencyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Default view set for 'Agency'

    Args:
        viewsets (ModelViewSet): Derives directly from ModelViewSet
    """

    queryset = Agency.objects.all().order_by("name")
    serializer_class = AgencySerializer
    permission_classes = [permissions.DjangoModelPermissions]


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Default view set for 'Group'

    Args:
        viewsets (ModelViewSet): Derives directly from ModelViewSet
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class ProgramViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Default view set for 'Program'

    Args:
        viewsets (ModelViewSet): Derives directly from ModelViewSet
    """

    queryset = Program.objects.all().order_by("name")
    serializer_class = ProgramSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Default view set for 'Question'

    Args:
        viewsets (ModelViewSet): Derives directly from ModelViewSet
    """

    queryset = Question.objects.all().order_by("description")
    serializer_class = QuestionSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class AnswerViewSet(viewsets.ModelViewSet):
    """
    Default view set for 'Answer'

    Args:
        viewsets (ModelViewSet): Derives directly from ModelViewSet
    """

    queryset = Answer.objects.all().order_by("user")
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

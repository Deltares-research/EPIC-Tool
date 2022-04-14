# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.response import Response

from epic_app.models.epic_questions import (
    Answer,
    EvolutionQuestion,
    LinkagesQuestion,
    NationalFrameworkQuestion,
)
from epic_app.models.epic_user import EpicUser
from epic_app.models.models import Agency, Area, Group, Program
from epic_app.serializers import (
    AgencySerializer,
    AnswerSerializer,
    AreaSerializer,
    EpicUserSerializer,
    EvolutionQuestionSerializer,
    GroupSerializer,
    LinkagesQuestionSerializer,
    NationalFrameworkQuestionSerializer,
    ProgramSerializer,
)


class EpicUserViewSet(viewsets.ModelViewSet):
    """
    Default view set for 'EpicUser'

    Args:
        viewsets (ModelViewSet): Derives directly from ModelViewSet
    """

    queryset = EpicUser.objects.all().order_by("username")
    serializer_class = EpicUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def _get_based_on_permissions(self, auth_user: EpicUser):
        if auth_user.is_staff or auth_user.is_superuser:
            return EpicUser.objects.all()
        else:
            return EpicUser.objects.filter(id=self.request.user.id)

    def list(self, request, *args, **kwargs):
        queryset = self._get_based_on_permissions(self.request.user)
        serializer = EpicUserSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self._get_based_on_permissions(self.request.user)
        user = get_object_or_404(queryset, pk=pk)
        serializer = EpicUserSerializer(user, context={"request": request})
        return Response(serializer.data)


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

    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class NationalFrameworkQuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NationalFrameworkQuestion.objects.all()
    serializer_class = NationalFrameworkQuestionSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class EvolutionQuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EvolutionQuestion.objects.all()
    serializer_class = EvolutionQuestionSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class LinkagesQuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LinkagesQuestion.objects.all()
    serializer_class = LinkagesQuestionSerializer
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

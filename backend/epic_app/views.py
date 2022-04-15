# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework import permissions, serializers, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.decorators import permission_classes as permission_decorator
from rest_framework.request import Request
from rest_framework.response import Response

from epic_app.models.epic_questions import (
    Answer,
    EvolutionQuestion,
    LinkagesQuestion,
    NationalFrameworkQuestion,
    Question,
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
    Acess point for CRUD operations on `EpicUser` table.
    """

    queryset = EpicUser.objects.all().order_by("username")
    serializer_class = EpicUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def _get_based_on_permissions(self, auth_user: EpicUser):
        if auth_user.is_staff or auth_user.is_superuser:
            return EpicUser.objects.all()
        else:
            return EpicUser.objects.filter(id=self.request.user.id)

    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        GET list `EpicUser`. When an admin all entries will be retrieved, otherwise only its own `EpicUser` one.

        Args:
            request (Request): API Request

        Returns:
            Response: Result of the queryset.
        """
        queryset = self._get_based_on_permissions(self.request.user)
        serializer = EpicUserSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def retrieve(self, request: Request, pk: str = None) -> Response:
        """
        GET detail `EpicUser`. When not an admin or self it will return a 404 response.

        Args:
            request (Request): API Request.
            pk (str, optional): Id of the `EpicUser` to retrieve. Defaults to None.

        Returns:
            Response: Result of the request.
        """
        queryset = self._get_based_on_permissions(self.request.user)
        user = get_object_or_404(queryset, pk=pk)
        serializer = EpicUserSerializer(user, context={"request": request})
        return Response(serializer.data)


class AreaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Acess point for CRUD operations on `Area` table.
    """

    queryset = Area.objects.all().order_by("name")
    serializer_class = AreaSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class AgencyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Acess point for CRUD operations on `Agency` table.
    """

    queryset = Agency.objects.all().order_by("name")
    serializer_class = AgencySerializer
    permission_classes = [permissions.DjangoModelPermissions]


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Acess point for CRUD operations on `Group` table.
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class ProgramViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Acess point for CRUD operations on `Program` table.
    """

    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def _get_question(
        self, request: Request, question_type: Question, pk: str = None
    ) -> Response:
        question_serializers = {
            NationalFrameworkQuestion: NationalFrameworkQuestionSerializer,
            EvolutionQuestion: EvolutionQuestionSerializer,
            LinkagesQuestion: LinkagesQuestionSerializer,
        }
        queryset: Question = question_type.objects.filter(program=pk)
        serializer: serializers.ModelSerializer = question_serializers[question_type](
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(
        detail=True,
        url_path="question-nationalframework",
        url_name="question_nationalframework",
    )
    def get_nationalframework_question(self, request: Request, pk: str = None):
        """
        GET List `NationalFrameworkQuestions` related to the program (`pk`).

        Args:
            request (Request): API Request.
            pk (str, optional): Id of the selected program. Defaults to None.

        Returns:
            Response: Result of the queryset.
        """
        return self._get_question(request, NationalFrameworkQuestion, pk)

    @action(
        detail=True,
        url_path="question-evolution",
        url_name="question_evolution",
    )
    def get_evolution_question(self, request: Request, pk: str = None):
        """
        GET List `EvolutionQuestion` related to the program (`pk`).

        Args:
            request (Request): API Request.
            pk (str, optional): Id of the selected program. Defaults to None.

        Returns:
            Response: Result of the queryset.
        """
        return self._get_question(request, EvolutionQuestion, pk)

    @action(
        detail=True,
        url_path="question-linkages",
        url_name="question_linkages",
    )
    def get_linkages_question(self, request: Request, pk: str = None):
        """
        GET List `LinkagesQuestion` related to the program (`pk`).

        Args:
            request (Request): API Request.
            pk (str, optional): Id of the selected program. Defaults to None.

        Returns:
            Response: Result of the queryset.
        """
        return self._get_question(request, LinkagesQuestion, pk)


class NationalFrameworkQuestionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Acess point for CRUD operations on `NationalFrameworkQuestion` table.
    """

    queryset = NationalFrameworkQuestion.objects.all()
    serializer_class = NationalFrameworkQuestionSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class EvolutionQuestionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Acess point for CRUD operations on `EvolutionQuestion` table.
    """

    queryset = EvolutionQuestion.objects.all()
    serializer_class = EvolutionQuestionSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class LinkagesQuestionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Acess point for CRUD operations on `LinkagesQuestion` table.
    """

    queryset = LinkagesQuestion.objects.all()
    serializer_class = LinkagesQuestionSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class AnswerViewSet(viewsets.ModelViewSet):
    """
    Acess point for CRUD operations on `Answer` table.
    """

    queryset = Answer.objects.all().order_by("user")
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

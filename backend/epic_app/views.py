# Create your views here.
from typing import List

from django.db.models import QuerySet
from rest_framework import permissions, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from epic_app.models.epic_answers import (
    Answer,
    MultipleChoiceAnswer,
    SingleChoiceAnswer,
    YesNoAnswer,
)
from epic_app.models.epic_questions import (
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
from epic_app.serializers.answer_serializer import (
    MultipleChoiceAnswerSerializer,
    SingleChoiceAnswerSerializer,
    YesNoAnswerSerializer,
)


class EpicUserViewSet(viewsets.ModelViewSet):
    """
    Acess point for CRUD operations on `EpicUser` table.
    """

    queryset = EpicUser.objects.all()
    serializer_class = EpicUserSerializer

    def get_permissions(self) -> List[permissions.BasePermission]:
        """
        `EpicUser` can only be created, updated or deleted when the authorized user is an admin.

        Returns:
            List[permissions.BasePermission]: List of permissions for the request being done.
        """
        if self.request.method in ["POST", "PUT", "DELETE"]:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self) -> QuerySet:
        """
        GET list `EpicUser`. When an admin all entries will be retrieved, otherwise only its own `EpicUser` one.

        Returns:
            QuerySet: Query instance containing the available `EpicUser` objects based on the authenticated user making the request.
        """
        if self.request.user.is_staff or self.request.user.is_superuser:
            return EpicUser.objects.all()
        return EpicUser.objects.filter(id=self.request.user.id)


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


# class AnswerViewSet(viewsets.ModelViewSet):
#     """
#     Acess point for CRUD operations on `Answer` table.
#     """

#     queryset = Answer.objects.all().order_by("user")
#     serializer_class = AnswerSerializer
#     permission_classes = [permissions.IsAuthenticated]


def answer_get_permissions(request: Request) -> List[permissions.BasePermission]:
    """
    `EpicUser` can only be created, updated or deleted when the authorized user is an admin.

    Returns:
        List[permissions.BasePermission]: List of permissions for the request being done.
    """
    if request.method in ["PUT", "DELETE"]:
        return [permissions.IsAdminUser()]
    return [permissions.IsAuthenticated()]


class YesNoAnswerViewSet(viewsets.ModelViewSet):
    queryset = YesNoAnswer.objects.all()
    serializer_class = YesNoAnswerSerializer

    def get_permissions(self):
        return answer_get_permissions(self.request)

    def get_queryset(self) -> QuerySet:
        """
        GET list `EpicUser`. When an admin all entries will be retrieved, otherwise only its own `EpicUser` one.

        Returns:
            QuerySet: Query instance containing the available `EpicUser` objects based on the authenticated user making the request.
        """
        if self.request.user.is_staff or self.request.user.is_superuser:
            return YesNoAnswer.objects.all()
        return YesNoAnswer.objects.filter(user=self.request.user)


class SingleChoiceAnswerViewSet(viewsets.ModelViewSet):
    queryset = SingleChoiceAnswer.objects.all()
    serializer_class = SingleChoiceAnswerSerializer

    def get_permissions(self):
        return answer_get_permissions(self.request)

    def get_queryset(self) -> QuerySet:
        """
        GET list `EpicUser`. When an admin all entries will be retrieved, otherwise only its own `EpicUser` one.

        Returns:
            QuerySet: Query instance containing the available `EpicUser` objects based on the authenticated user making the request.
        """
        if self.request.user.is_staff or self.request.user.is_superuser:
            return SingleChoiceAnswer.objects.all()
        return SingleChoiceAnswer.objects.filter(user=self.request.user)


class MultipleChoiceAnswerViewSet(viewsets.ModelViewSet):
    queryset = MultipleChoiceAnswer.objects.all()
    serializer_class = MultipleChoiceAnswerSerializer

    def get_permissions(self):
        return answer_get_permissions(self.request)

    def get_queryset(self) -> QuerySet:
        """
        GET list `EpicUser`. When an admin all entries will be retrieved, otherwise only its own `EpicUser` one.

        Returns:
            QuerySet: Query instance containing the available `EpicUser` objects based on the authenticated user making the request.
        """
        if self.request.user.is_staff or self.request.user.is_superuser:
            return MultipleChoiceAnswer.objects.all()
        return MultipleChoiceAnswer.objects.filter(user=self.request.user)

# Create your views here.
from typing import List, Type, Union

from django.db.models import QuerySet
from django.http import HttpRequest
from rest_framework import permissions, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from epic_app.epic_permissions import IsAdminOrSelfUser
from epic_app.models.epic_answers import (
    Answer,
    MultipleChoiceAnswer,
    SingleChoiceAnswer,
    YesNoAnswer,
)
from epic_app.models.epic_questions import (
    EvolutionQuestion,
    KeyAgencyActionsQuestion,
    LinkagesQuestion,
    NationalFrameworkQuestion,
    Question,
)
from epic_app.models.epic_user import EpicOrganization, EpicUser
from epic_app.models.models import Agency, Area, Group, Program
from epic_app.serializers import (
    AgencySerializer,
    AreaSerializer,
    EpicOrganizationSerializer,
    EpicUserSerializer,
    EvolutionQuestionSerializer,
    GroupSerializer,
    LinkagesQuestionSerializer,
    NationalFrameworkQuestionSerializer,
    ProgramSerializer,
)
from epic_app.serializers.answer_serializer import (
    AnswerSerializer,
    MultipleChoiceAnswerSerializer,
    SingleChoiceAnswerSerializer,
    YesNoAnswerSerializer,
)
from epic_app.serializers.question_serializer import (
    KeyAgencyQuestionSerializer,
    QuestionSerializer,
)
from epic_app.utils import get_model_subtypes


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
        if self.request.method in ["POST", "DELETE"]:
            return [permissions.IsAdminUser()]
        if self.request.method == "PUT":
            return [IsAdminOrSelfUser()]
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

    @action(
        methods=["put"],
        detail=True,
        permission_classes=[IsAdminOrSelfUser],
        url_path="change-password",
        url_name="change_password",
    )
    def put_epicuser_password(self, request: Request, pk: str = None):
        """
        Updates the field `password` for an `EpicUser` with the given `pk`.

        Args:
            request (Request): HTTP Request.
            pk (str, optional): Field representing the `pk` of an `EpicUser`. Defaults to None.

        Returns:
            Response: Result of the queryset.
        """
        serializer: EpicUserSerializer = self.get_serializer(
            EpicUser.objects.filter(pk=pk).first(), data=request.data, partial=True
        )
        serializer.is_valid()
        serializer.save()
        return Response(data=serializer.data)


class EpicOrganizationViewSet(viewsets.ModelViewSet):
    """
    Acess point for CRUD operations on `EpicOrganization` table.
    """

    queryset = EpicOrganization.objects.all()
    serializer_class = EpicOrganizationSerializer
    permission_classes = [permissions.IsAdminUser]


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
            KeyAgencyActionsQuestion: KeyAgencyQuestionSerializer,
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
        GET List `NationalFrameworkQuestion` related to the program (`pk`).

        Args:
            request (Request): API Request.
            pk (str, optional): Id of the selected program. Defaults to None.

        Returns:
            Response: Result of the queryset.
        """
        return self._get_question(request, NationalFrameworkQuestion, pk)

    @action(
        detail=True,
        url_path="question-keyagencyactions",
        url_name="question_keyagencyactions",
    )
    def get_keyagencyactions_question(self, request: Request, pk: str = None):
        """
        GET List `KeyAgencyActionsQuestion` related to the program (`pk`).

        Args:
            request (Request): API Request.
            pk (str, optional): Id of the selected program. Defaults to None.

        Returns:
            Response: Result of the queryset.
        """
        return self._get_question(request, KeyAgencyActionsQuestion, pk)

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


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permissiion_classes = [permissions.DjangoModelPermissions]

    def _get_question_type(self, pk: str) -> Question:
        question_subtypes = get_model_subtypes(Question)
        q_type = next(
            (q_t for q_t in question_subtypes if q_t.objects.filter(pk=pk).exists()),
            None,
        )
        return q_type

    def _get_answer_type(self, question_pk: str) -> Type[Answer]:
        q_type = self._get_question_type(question_pk)
        answer_subtypes: List[Type[Answer]] = get_model_subtypes(Answer)
        a_type = next(
            (
                a_t
                for a_t in answer_subtypes
                if q_type in a_t._get_supported_questions()
            ),
            None,
        )
        return a_type

    def _get_epic_users_queryset(
        self, request: HttpRequest
    ) -> Union[QuerySet, List[EpicUser]]:
        """
        Gets the query needed to retrieve data for all involved users.
        """
        if not EpicUser.objects.filter(pk=request.user.pk).exists():
            if not (request.user.is_superuser or request.user.is_staff):
                raise ValueError(
                    "This request needs to be done by an `EpicUser` or a `superuser`."
                )
            return EpicUser.objects.all()
        return EpicUser.objects.filter(pk=request.user.pk)

    def retrieve(self, request, pk: str, *args, **kwargs):
        """
        Retrieves a `Question` serialized as its subtype definition.
        """
        # Find to which question subtype it belongs.
        q_type = self._get_question_type(pk)
        q_serializer_type = QuestionSerializer.get_concrete_serializer(q_type)
        queryset = q_type.objects.filter(pk=pk)
        q_serializer = q_serializer_type(
            queryset, many=True, context={"request": request}
        )

        return Response(q_serializer.data)

    @action(detail=True, url_path="answers", url_name="answers")
    def retrieve_answers(self, request: HttpRequest, pk: str = None) -> QuerySet:
        """
        Retrieves the `answers` for the given `question`.
        ASSUMPTION: The request is done with an `EpicUser`.

        Args:
            request (HttpRequest): Request from the client.
            pk (str, optional): `Answer` id. Defaults to None.
        """

        def get_user_answer(epic_user: EpicUser) -> Answer:
            a_instance, _ = a_type.objects.get_or_create(
                question=Question.objects.get(pk=pk), user=epic_user
            )
            return a_instance

        e_users = self._get_epic_users_queryset(request)
        a_type = self._get_answer_type(question_pk=pk)
        a_serializer_type = AnswerSerializer.get_concrete_serializer(a_type)
        a_instances = [get_user_answer(e_user) for e_user in e_users]
        a_serializer = a_serializer_type(
            a_instances, many=True, context={"request": request}
        )
        return Response(a_serializer.data)


def answer_get_permissions(request: Request) -> List[permissions.BasePermission]:
    """
    `EpicUser` can only be created, updated or deleted when the authorized user is an admin.

    Returns:
        List[permissions.BasePermission]: List of permissions for the request being done.
    """
    if not request.data.get("user", None):
        request.data["user"] = request.user.id
    if request.method in ["PUT", "DELETE"]:
        return [permissions.IsAdminUser()]
    return [permissions.IsAuthenticated()]


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def get_permissions(self):
        return answer_get_permissions(self.request)

    def get_queryset(self) -> Union[QuerySet, List[Answer]]:
        """
        GET list of `Answers` based on the user doing the request.  When `superuser` or `staff` all entries will be retrieved, otherwise only entries where `epic_user.pk` matches `request.user.pk`.

        Returns:
            Union[QuerySet, List[Answer]]: `Answer` subset depending on the requesting `EpicUser` permissions.
        """
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Answer.objects.all()
        return Answer.objects.filter(user=self.request.user)

    def retrieve(self, request, pk: str, *args, **kwargs):
        """
        RETRIEVE a single `Answer` which is serialized based on its subtype.
        """
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, pk: str, *args, **kwargs):
        """
        UPDATE a single `Answer`. It assumes the given data matches the expected subtype.
        """
        return super().update(request, *args, **kwargs)


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

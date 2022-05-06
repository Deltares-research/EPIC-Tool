# Create your views here.
from typing import List, Type, Union

from django.db import models
from rest_framework import permissions, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from epic_app import epic_permissions
from epic_app import serializers as epic_serializer
from epic_app.models.epic_answers import Answer
from epic_app.models.epic_questions import (
    EvolutionQuestion,
    KeyAgencyActionsQuestion,
    LinkagesQuestion,
    NationalFrameworkQuestion,
    Question,
)
from epic_app.models.epic_user import EpicOrganization, EpicUser
from epic_app.models.models import Agency, Area, Group, Program
from epic_app.utils import get_submodel_type, get_submodel_type_list


class EpicUserViewSet(viewsets.ModelViewSet):
    """
    Acess point for CRUD operations on `EpicUser` table.
    """

    queryset = EpicUser.objects.all()
    serializer_class = epic_serializer.EpicUserSerializer

    def get_permissions(self) -> List[permissions.BasePermission]:
        """
        `EpicUser` can only be created, updated or deleted when the authorized user is an admin.

        Returns:
            List[permissions.BasePermission]: List of permissions for the request being done.
        """
        if self.request.method in ["POST", "DELETE"]:
            return [permissions.IsAdminUser()]
        if self.request.method in ["PUT", "PATCH"]:
            return [epic_permissions.IsAdminOrSelfUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self) -> models.QuerySet:
        """
        GET list `EpicUser`. When an admin all entries will be retrieved, otherwise only its own `EpicUser` one.

        Returns:
            models.QuerySet: Query instance containing the available `EpicUser` objects based on the authenticated user making the request.
        """
        if self.request.user.is_staff or self.request.user.is_superuser:
            return EpicUser.objects.all()
        return EpicUser.objects.filter(id=self.request.user.id)

    @action(
        methods=["put"],
        detail=True,
        permission_classes=[epic_permissions.IsAdminOrSelfUser],
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
        serializer: epic_serializer.EpicUserSerializer = self.get_serializer(
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
    serializer_class = epic_serializer.EpicOrganizationSerializer
    permission_classes = [permissions.IsAdminUser]


class AreaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Acess point for CRUD operations on `Area` table.
    """

    queryset = Area.objects.all().order_by("name")
    serializer_class = epic_serializer.AreaSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class AgencyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Acess point for CRUD operations on `Agency` table.
    """

    queryset = Agency.objects.all().order_by("name")
    serializer_class = epic_serializer.AgencySerializer
    permission_classes = [permissions.DjangoModelPermissions]


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Acess point for CRUD operations on `Group` table.
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = epic_serializer.GroupSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class ProgramViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Acess point for CRUD operations on `Program` table.
    """

    queryset = Program.objects.all()
    serializer_class = epic_serializer.ProgramSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    @action(detail=True, url_path="progress", url_name="progress")
    def get_progress(self, request: Request, pk: str = None) -> Response:
        """
        Gets the percentage of answered questions for the `Program` with provided `id` and the `EpicUser` currently logged in.
        Note that the user will be fetched in the `ProgressSerializer` by using the data stored in `context`.

        Args:
            request (Request): API Request.
            pk (str, optional): `Program` Id. Defaults to None.

        Returns:
            Response: Result of the serialised request to `ProgressSerializer`.
        """
        request.data["user"] = request.user.epic_user
        serializer = epic_serializer.ProgressSerializer(
            Program.objects.get(pk=pk), context={"request": request}
        )
        return Response(serializer.data)

    def _get_question(
        self, request: Request, question_type: Question, pk: str = None
    ) -> Response:
        question_serializers = {
            NationalFrameworkQuestion: epic_serializer.NationalFrameworkQuestionSerializer,
            EvolutionQuestion: epic_serializer.EvolutionQuestionSerializer,
            LinkagesQuestion: epic_serializer.LinkagesQuestionSerializer,
            KeyAgencyActionsQuestion: epic_serializer.KeyAgencyQuestionSerializer,
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
    serializer_class = epic_serializer.QuestionSerializer
    permissiion_classes = [permissions.DjangoModelPermissions]

    @staticmethod
    def _get_related_answer_type(question_pk: str) -> Type[Answer]:
        q_type = get_submodel_type(Question, question_pk)
        answer_subtypes: List[Type[Answer]] = get_submodel_type_list(Answer)
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
        self, request: Request
    ) -> Union[models.QuerySet, List[EpicUser]]:
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
        q_type = get_submodel_type(Question, pk)
        q_serializer_type = epic_serializer.QuestionSerializer.get_concrete_serializer(
            q_type
        )
        queryset = q_type.objects.filter(pk=pk)
        q_serializer = q_serializer_type(
            queryset, many=True, context={"request": request}
        )

        return Response(q_serializer.data)

    @action(detail=True, url_path="answers", url_name="answers")
    def retrieve_answers(self, request: Request, pk: str = None) -> models.QuerySet:
        """
        Retrieves the `answers` for the given `question`.
        ASSUMPTION: The request is done with an `EpicUser`.

        Args:
            request (Request): Request from the client.
            pk (str, optional): `Answer` id. Defaults to None.
        """

        def get_user_answer(epic_user: EpicUser) -> Answer:
            a_instance, _ = a_type.objects.get_or_create(
                question=Question.objects.get(pk=pk), user=epic_user
            )
            return a_instance

        e_users = self._get_epic_users_queryset(request)
        a_type = self._get_related_answer_type(question_pk=pk)
        a_serializer_type = epic_serializer.AnswerSerializer.get_concrete_serializer(
            a_type
        )
        a_instances = [get_user_answer(e_user) for e_user in e_users]
        a_serializer = a_serializer_type(
            a_instances, many=True, context={"request": request}
        )
        return Response(a_serializer.data)


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = epic_serializer.AnswerSerializer

    def get_permissions(self):
        if not self.request.data.get("user", None):
            self.request.data["user"] = self.request.user.id
        if self.request.method in ["PUT", "DELETE", "PATCH"]:
            return [epic_permissions.IsAdminOrInstanceOwner()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self) -> Union[models.QuerySet, List[Answer]]:
        """
        GET list of `Answers` based on the user doing the request.  When `superuser` or `staff` all entries will be retrieved, otherwise only entries where `epic_user.pk` matches `request.user.pk`.

        Returns:
            Union[models.QuerySet, List[Answer]]: `Answer` subset depending on the requesting `EpicUser` permissions.
        """
        return self._filter_queryset(Answer)

    def _filter_queryset(
        self, answer_type: Type[Answer]
    ) -> Union[models.QuerySet, List[Answer]]:
        """
        Filter querysets to prevent unauthorized `EpicUsers` from retrieving `Answers` from others.
        """
        if self.request.user.is_staff or self.request.user.is_superuser:
            return answer_type.objects.all()
        return answer_type.objects.filter(user=self.request.user)

    def retrieve(self, request, pk: str, *args, **kwargs):
        """
        RETRIEVE a single `Answer` which is serialized based on its subtype.
        """
        a_subtype = get_submodel_type(Answer, pk)
        a_serializer_type = epic_serializer.AnswerSerializer.get_concrete_serializer(
            a_subtype
        )
        a_serializer = a_serializer_type(
            self._filter_queryset(a_subtype).get(pk=pk), context={"request": request}
        )
        return Response(data=a_serializer.data)

    def _get_update_request(self, request: Request, pk: str) -> Request:
        a_subtype = get_submodel_type(Answer, pk)
        self.serializer_class = (
            epic_serializer.AnswerSerializer.get_concrete_serializer(a_subtype)
        )
        self.queryset = self._filter_queryset(a_subtype).get(pk=pk)
        # Prevent admins from replacing the user in the partial_update
        request.data["user"] = self.queryset.user_id
        return request

    def update(self, request, pk: str, *args, **kwargs):
        """
        UPDATE a single `Answer`. It assumes the given data matches the expected subtype.
        """
        return super().update(
            self._get_update_request(request, pk), pk, *args, **kwargs
        )

    def partial_update(self, request, pk: str, *args, **kwargs):
        """
        PATCH a single `Answer`. It assumes the given data matches the expected subtype.
        """

        return super().partial_update(
            self._get_update_request(request, pk), pk, *args, **kwargs
        )

    def create(self, request, *args, **kwargs):
        """
        CREATE a new `Answer` using the subtype associated serializer.
        """
        a_subtype = QuestionViewSet._get_related_answer_type(request.data["question"])
        self.serializer_class = (
            epic_serializer.AnswerSerializer.get_concrete_serializer(a_subtype)
        )
        return super().create(request, *args, **kwargs)

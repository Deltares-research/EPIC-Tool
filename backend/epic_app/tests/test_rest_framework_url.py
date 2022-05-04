import json
from typing import Callable, Type

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from epic_app.models.epic_answers import (
    Answer,
    MultipleChoiceAnswer,
    SingleChoiceAnswer,
    YesNoAnswer,
    YesNoAnswerType,
)
from epic_app.models.epic_questions import EvolutionChoiceType, Question
from epic_app.models.epic_user import EpicOrganization, EpicUser
from epic_app.models.models import Program
from epic_app.tests.epic_db_fixture import epic_test_db
from epic_app.utils import get_submodel_type_list


@pytest.fixture(autouse=True)
def rest_framework_url_fixture(epic_test_db: pytest.fixture):
    """
    Dummy fixture just to load a default db from dummy_db.

    Args:
        epic_test_db (pytest.fixture): Fixture to load for the whole file tests.
    """
    pass


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
def get_admin_user() -> User:
    admin_user: User = User.objects.filter(username="admin").first()
    assert admin_user.is_superuser
    assert admin_user.is_staff
    return admin_user


@pytest.mark.django_db
def get_epic_user(username: str) -> EpicUser:
    epic_user: EpicUser = EpicUser.objects.filter(username=username).first()
    assert not epic_user.is_superuser
    assert not epic_user.is_staff
    return epic_user


@pytest.mark.django_db
def set_user_auth_token(api_client: APIClient, username: str) -> str:
    epic_user = User.objects.filter(username=username).first()
    assert epic_user
    token_str = "Token " + epic_user.auth_token.key

    # Run request.
    api_client.credentials(HTTP_AUTHORIZATION=token_str)


@pytest.mark.django_db
class TestEpicUserTokenAuthRequest:
    url_root = "/api/token-auth/"

    @pytest.mark.parametrize(
        "epic_username",
        [
            pytest.param(
                "Palpatine",
                id="Non admins cannot retrieve other users.",
            ),
            pytest.param(
                "admin",
                id="Admins can retrieve other users.",
            ),
        ],
    )
    @pytest.mark.parametrize(
        "url_suffix, response_code",
        [
            pytest.param("", 405, id="List all"),
            pytest.param("2/", 404, id="Retrieve epic_user id=2"),
        ],
    )
    def test_GET_token_auth(
        self,
        epic_username: str,
        url_suffix: str,
        response_code: int,
        api_client: APIClient,
    ):
        # Define test data.
        set_user_auth_token(api_client, epic_username)
        response = api_client.get(self.url_root + url_suffix)

        # Verify final exepctations.
        assert response.status_code == response_code

    @pytest.mark.parametrize(
        "username, password, expected_status",
        [
            pytest.param("Palpatine", "palpatine", 200, id="Correct user and password"),
            pytest.param("Darth Sidious", "palpatine", 400, id="Incorrect user"),
            pytest.param("Palpatine", "darth_sidius", 400, id="Incorrect password"),
        ],
    )
    def test_POST_token_auth(
        self, api_client: APIClient, username: str, password: str, expected_status: int
    ):
        # Set test data
        data = {"username": username, "password": password}

        # Run request.
        response = api_client.post(self.url_root, data, format="json")

        # Verify final expectations.
        assert response.status_code == expected_status
        if expected_status == 200:
            assert response.data.get("token") is not None
        else:
            assert response.data.get("token") is None


@pytest.mark.django_db
class TestEpicUserViewSet:
    url_root = "/api/epicuser/"

    @pytest.mark.parametrize(
        "epic_username, multiple_entries",
        [
            pytest.param(
                "Palpatine",
                False,
                id="Non admins cannot retrieve other users.",
            ),
            pytest.param(
                "admin",
                True,
                id="Admins can retrieve other users.",
            ),
        ],
    )
    def test_GET_list_epic_user(
        self,
        epic_username: str,
        multiple_entries: bool,
        api_client: APIClient,
    ):
        # Define test data.
        set_user_auth_token(api_client, epic_username)
        response = api_client.get(self.url_root)

        # Verify final exepctations.
        assert response.status_code == 200
        if not multiple_entries:
            assert len(response.data) == 1
        else:
            assert len(response.data) > 1

    anakin_json_data = {
        "url": "http://testserver/api/epicuser/3/",
        "id": 3,
        "username": "Anakin",
        "organization": 1,
        "selected_programs": [2, 4],
    }

    @pytest.mark.parametrize(
        "epic_username, find_username, expected_response",
        [
            pytest.param(
                "Palpatine",
                "Anakin",
                dict(status_code=404, content={"detail": "Not found."}),
                id="Non admins cannot retrieve other users.",
            ),
            pytest.param(
                "Anakin",
                "Anakin",
                dict(status_code=200, content=anakin_json_data),
                id="Non admins can retrieve themselves.",
            ),
            pytest.param(
                "admin",
                "Anakin",
                dict(status_code=200, content=anakin_json_data),
                id="Admins can retrieve other users.",
            ),
        ],
    )
    def test_GET_detail_epic_user(
        self,
        epic_username: str,
        find_username: str,
        expected_response: dict,
        api_client: APIClient,
    ):
        # Define test data.
        user_found = get_epic_user(find_username)
        url = f"{self.url_root}{user_found.pk}/"

        # Run request.
        set_user_auth_token(api_client, epic_username)
        response = api_client.get(url)

        # Verify final exepctations.
        assert response.status_code == expected_response["status_code"]
        assert json.loads(response.content) == expected_response["content"]

    @pytest.mark.parametrize(
        "epic_username",
        [
            pytest.param(None, id="No user authenticated"),
            pytest.param("Palpatine", id="Authenticated USER"),
        ],
    )
    def test_POST_when_not_admin_returns_error(
        self, epic_username: str, api_client: APIClient
    ):
        """
        Note: This test is to verify that we DO NOT allow user creation unless
        from an admin. In the future we might allow anyone to create new ones.
        """
        ck_username = "ClarkKent"
        data_dict = {
            "username": ck_username,
            "password": "IamSup3rm4n!",
            "organization": "Daily Planet",
        }
        assert not EpicUser.objects.filter(username=ck_username).exists()

        # Run request.
        if epic_username:
            set_user_auth_token(api_client, epic_username)
        response = api_client.post(self.url_root, data_dict, format="json")

        # Verify final expectations.
        assert response.status_code in [
            403,
            405,
        ], "It should NOT be possible to create a user."
        assert not EpicUser.objects.filter(
            username=ck_username
        ).exists(), "User was created despite not having to."

    def test_POST_when_admin_returns_created(self, api_client: APIClient):
        ck_username = "ClarkKent"
        data_dict = {
            "username": ck_username,
            "password": "IamSup3rm4n!",
            "organization": EpicOrganization.objects.last().id,
        }
        assert not EpicUser.objects.filter(username=ck_username).exists()

        # Run request.
        set_user_auth_token(api_client, "admin")
        response = api_client.post(self.url_root, data_dict, format="json")

        # Verify final expectations.
        assert response.status_code == 201
        assert EpicUser.objects.filter(
            username=ck_username
        ).exists(), "User was not created despite succesful response."

    @pytest.mark.parametrize(
        "epic_username, find_username, expected_response",
        [
            pytest.param(
                "Palpatine",
                "Anakin",
                dict(status_code=403, content={"detail": "Not found."}),
                id="Non admins cannot update other users' password.",
            ),
            pytest.param(
                "Anakin",
                "Anakin",
                dict(status_code=200, content=anakin_json_data),
                id="Non admins can update their own password.",
            ),
            pytest.param(
                "admin",
                "Anakin",
                dict(status_code=200, content=anakin_json_data),
                id="Admins can update other users' password.",
            ),
        ],
    )
    def test_PUT_epic_user_password(
        self,
        epic_username: str,
        find_username: str,
        expected_response: dict,
        api_client: APIClient,
    ):
        user_found = get_epic_user(find_username)
        previous_pass = user_found.password
        changepass_url = "change-password/"
        url = f"{self.url_root}{user_found.pk}/" + changepass_url
        data_dict = {
            "password": "IamSup3rm4n!",
        }

        # Run request.
        set_user_auth_token(api_client, epic_username)
        response = api_client.put(url, data_dict, format="json")

        # Verify final exepctations.
        assert response.status_code == expected_response["status_code"]
        if response.status_code == 200:
            assert previous_pass != get_epic_user(find_username).password


@pytest.mark.django_db
class TestAreaViewSet:
    url_root = "/api/area/"

    @pytest.mark.parametrize(
        "epic_username",
        [
            pytest.param(
                "Palpatine",
                id="Non admins user.",
            ),
            pytest.param(
                "admin",
                id="Admins user.",
            ),
        ],
    )
    @pytest.mark.parametrize(
        "url_suffix, expected_entries",
        [
            pytest.param("", 2, id="get-list"),
            pytest.param("1/", 4, id="get-retrieve (Area 'alpha' with 4 groups)"),
        ],
    )
    def test_GET_area(
        self,
        epic_username: str,
        url_suffix: str,
        expected_entries: int,
        api_client: APIClient,
    ):
        full_url = self.url_root + url_suffix
        # Run request.
        set_user_auth_token(api_client, epic_username)
        response = api_client.get(full_url)

        # Verify final exepctations.
        assert response.status_code == 200
        assert len(response.data) == expected_entries


@pytest.mark.django_db
class TestAgencyViewSet:
    url_root = "/api/agency/"

    @pytest.mark.parametrize(
        "epic_username",
        [
            pytest.param(
                "Palpatine",
                id="Non admins user.",
            ),
            pytest.param(
                "admin",
                id="Admins user.",
            ),
        ],
    )
    @pytest.mark.parametrize(
        "url_suffix, expected_entries",
        [
            pytest.param("", 4, id="get-list"),
            pytest.param("1/", 4, id="get-retrieve (Agency 'T.I.A.' with 4 fields)"),
        ],
    )
    def test_GET_agency(
        self,
        epic_username: str,
        url_suffix: str,
        expected_entries: int,
        api_client: APIClient,
    ):
        full_url = self.url_root + url_suffix
        # Run request.
        set_user_auth_token(api_client, epic_username)
        response = api_client.get(full_url)

        # Verify final exepctations.
        assert response.status_code == 200
        assert len(response.data) == expected_entries


@pytest.mark.django_db
class TestGroupViewSet:
    url_root = "/api/group/"

    @pytest.mark.parametrize(
        "epic_username",
        [
            pytest.param(
                "Palpatine",
                id="Non admins user.",
            ),
            pytest.param(
                "admin",
                id="Admins user.",
            ),
        ],
    )
    @pytest.mark.parametrize(
        "url_suffix, expected_entries",
        [
            pytest.param("", 3, id="get-list"),
            pytest.param("1/", 5, id="get-retrieve (Group 'first' with 5 fields)"),
        ],
    )
    def test_GET_group(
        self,
        epic_username: str,
        url_suffix: str,
        expected_entries: int,
        api_client: APIClient,
    ):
        full_url = self.url_root + url_suffix
        # Run request.
        set_user_auth_token(api_client, epic_username)
        response = api_client.get(full_url)

        # Verify final exepctations.
        assert response.status_code == 200
        assert len(response.data) == expected_entries


@pytest.mark.django_db
class TestProgramViewSet:
    url_root = "/api/program/"

    @pytest.mark.parametrize(
        "epic_username",
        [
            pytest.param(
                "Palpatine",
                id="Non admins user.",
            ),
            pytest.param(
                "admin",
                id="Admins user.",
            ),
        ],
    )
    @pytest.mark.parametrize(
        "url_suffix, expected_entries",
        [
            pytest.param("", 5, id="get-list"),
            pytest.param("1/", 7, id="get-retrieve (Program 'a' with 9 fields)"),
        ],
    )
    def test_GET_program(
        self,
        epic_username: str,
        url_suffix: str,
        expected_entries: int,
        api_client: APIClient,
    ):
        full_url = self.url_root + url_suffix
        # Run request.
        set_user_auth_token(api_client, epic_username)
        response = api_client.get(full_url)

        # Verify final exepctations.
        assert response.status_code == 200
        assert len(response.data) == expected_entries

    @pytest.mark.parametrize(
        "url_suffix, expected_entries",
        [
            pytest.param(
                "question-nationalframework/", 2, id="LIST NationalFramework Questions"
            ),
            pytest.param("question-evolution/", 2, id="LIST Evolution Questions"),
            pytest.param("question-linkages/", 1, id="LIST Linkages Questions"),
            pytest.param(
                "question-keyagencyactions/", 1, id="LIST KeyAgencyActions Questions"
            ),
        ],
    )
    def test_GET_list_program_questions(
        self,
        url_suffix: str,
        expected_entries: int,
        api_client: APIClient,
    ):
        # Program a has 5 questions (2xNFQ, 2xEVO, 1xLNK)
        a_program: Program = Program.objects.filter(name="a").first()
        full_url = self.url_root + f"{a_program.pk}/" + url_suffix
        # Run request.
        set_user_auth_token(api_client, "Palpatine")
        response = api_client.get(full_url)

        # Verify final exepctations.
        assert response.status_code == 200
        assert len(response.data) == expected_entries


@pytest.mark.django_db
class TestQuestionViewSet:
    url_root = "/api/question/"
    q_subtypes = get_submodel_type_list(Question)

    @pytest.mark.parametrize("username", [("Palpatine"), ("admin")])
    def test_GET_question(self, username: str, api_client: APIClient):
        set_user_auth_token(api_client, username)
        response = api_client.get(self.url_root)

        # Verify final expectations.
        assert response.status_code == 200
        assert len(response.data) == 6

    @pytest.mark.parametrize("username", [("Palpatine"), ("admin")])
    @pytest.mark.parametrize("q_type", q_subtypes)
    def test_RETRIEVE_question(
        self, username: str, q_type: Type[Question], api_client: APIClient
    ):
        q_pk = q_type.objects.all().first().pk
        full_url = self.url_root + str(q_pk) + "/"
        set_user_auth_token(api_client, username)
        response = api_client.get(full_url)

        # Verify final expectations.
        assert response.status_code == 200
        assert len(response.data) == 1

    @pytest.mark.parametrize("q_type", q_subtypes)
    def test_RETRIEVE_answers_for_epic_user(
        self, q_type: Type[Question], api_client: APIClient
    ):
        # Define test data.
        q_pk = q_type.objects.all().first().pk
        full_url = self.url_root + str(q_pk) + "/answers/"

        # Remove all previous answers, the call should create a new one
        Answer.objects.all().delete()

        # Run test
        set_user_auth_token(api_client, "Palpatine")
        response = api_client.get(full_url)

        # Verify final expectations.
        assert response.status_code == 200
        # One user = One (new) answer
        assert len(response.data) == 1

    @pytest.mark.parametrize("q_type", q_subtypes)
    def test_RETRIEVE_answers_for_superuser(
        self, q_type: Type[Question], api_client: APIClient
    ):
        # Define test data.
        q_pk = q_type.objects.all().first().pk
        full_url = self.url_root + str(q_pk) + "/answers/"
        set_user_auth_token(api_client, "admin")
        response = api_client.get(full_url)

        # Verify final expectations.
        assert response.status_code == 200
        # As many answers as users there are
        assert len(response.data) == len(EpicUser.objects.all())


@pytest.mark.django_db
class TestAnswerViewSet:
    url_root = "/api/answer/"
    a_subtypes = get_submodel_type_list(Answer)

    def _compare_answer_fields(
        self,
        a_instance: Answer,
        json_data: dict,
        compare_expression: Callable[[Answer, dict], bool],
    ):
        if isinstance(a_instance, MultipleChoiceAnswer):
            a_instance_selected_programs = [
                p.id for p in a_instance.selected_programs.all()
            ]
            assert compare_expression(
                a_instance_selected_programs, json_data["selected_programs"]
            )
            # We don't need to compare the rest as there are no more fields to compare.
            return
        for answer_field, answer_value in json_data.items():
            assert compare_expression(
                str(a_instance.__dict__[answer_field]), str(answer_value)
            )

    @pytest.fixture
    def _answers_fixture(self) -> dict:
        self.anakin = EpicUser.objects.filter(username="Anakin").first()
        self.yna = YesNoAnswer.objects.create(
            user=self.anakin,
            question=Question.objects.filter(pk=1).first(),
            short_answer=YesNoAnswerType.NO,
            justify_answer="Laboris proident enim dolore ullamco voluptate nisi labore laborum ut qui adipisicing occaecat exercitation culpa.",
        )
        self.sca = SingleChoiceAnswer.objects.create(
            user=self.anakin,
            question=Question.objects.filter(pk=3).first(),
            selected_choice=EvolutionChoiceType.EFFECTIVE,
            justify_answer="Ea ut ipsum deserunt culpa laborum excepteur laboris ad adipisicing ad officia laboris.",
        )
        self.mca = MultipleChoiceAnswer(
            user=self.anakin,
            question=Question.objects.filter(pk=5).first(),
        )
        self.mca.save()
        self.mca.selected_programs.add(4, 2)
        return {
            YesNoAnswer: {
                "url": "http://testserver/api/answer/1/",
                "id": 1,
                "user": 3,
                "question": 1,
                "short_answer": "N",
                "justify_answer": "Laboris proident enim dolore ullamco voluptate nisi labore laborum ut qui adipisicing occaecat exercitation culpa.",
            },
            SingleChoiceAnswer: {
                "url": "http://testserver/api/answer/2/",
                "id": 2,
                "user": 3,
                "question": 3,
                "selected_choice": str(EvolutionChoiceType.EFFECTIVE),
                "justify_answer": "Ea ut ipsum deserunt culpa laborum excepteur laboris ad adipisicing ad officia laboris.",
            },
            MultipleChoiceAnswer: {
                "url": "http://testserver/api/answer/3/",
                "id": 3,
                "question": 5,
                "selected_programs": [2, 4],
                "user": 3,
            },
        }

    @pytest.fixture(autouse=False)
    def _answers_update_fixture(self) -> dict:
        """
        Returns a dictionary of values that can be used to return the values generated at the `_answer_fixture` method.
        """
        return {
            YesNoAnswer: dict(
                short_answer=str(YesNoAnswerType.YES),
                justify_answer="For my own reasons",
            ),
            SingleChoiceAnswer: dict(
                selected_choice=str(EvolutionChoiceType.ENGAGED),
                justify_answer="For the lulz",
            ),
            MultipleChoiceAnswer: dict(selected_programs=[3, 4]),
        }

    answer_fixture_users = [
        pytest.param("Anakin", id="Answer owner"),
        pytest.param("admin", id="Admin (super_user / staff)"),
    ]

    @pytest.mark.parametrize("username", answer_fixture_users)
    def test_GET_answer_authorized_user(
        self, username: str, api_client: APIClient, _answers_fixture: dict
    ):
        # Define test data, only url, id, user and question available when GET-LIST
        expected_values = [
            dict(
                url=a_f["url"], id=a_f["id"], user=a_f["user"], question=a_f["question"]
            )
            for a_f in _answers_fixture.values()
        ]
        # Run test
        set_user_auth_token(api_client, username)
        response = api_client.get(self.url_root)

        # Verify final expectations.
        assert response.status_code == 200
        assert len(response.data) == 3
        assert json.dumps(response.data) == json.dumps(expected_values)

    def test_GET_answer_non_authorized_user(
        self, api_client: APIClient, _answers_fixture: dict
    ):
        # Run test
        set_user_auth_token(api_client, "Palpatine")
        response = api_client.get(self.url_root)

        # Verify final expectations.
        assert response.status_code == 200
        assert len(response.data) == 0

    @pytest.mark.parametrize("username", answer_fixture_users)
    @pytest.mark.parametrize("answer_type", get_submodel_type_list(Answer))
    def test_RETRIEVE_answer_authorized_user(
        self,
        username: str,
        answer_type: Type[Answer],
        api_client: APIClient,
        _answers_fixture: dict,
    ):
        expected_values = _answers_fixture[answer_type]
        full_url = self.url_root + str(expected_values["id"]) + "/"
        # Remove "url" as it's not expected in the detailed view.
        expected_values.pop("url")

        # Run test
        set_user_auth_token(api_client, username)
        response = api_client.get(full_url)

        # Verify final expectations.
        assert response.status_code == 200
        assert response.data == expected_values

    @pytest.mark.parametrize("answer_type", get_submodel_type_list(Answer))
    def test_RETRIEVE_answer_unauthorized_user(
        self,
        answer_type: Type[Answer],
        api_client: APIClient,
        _answers_fixture: dict,
    ):
        expected_values = _answers_fixture[answer_type]
        full_url = self.url_root + str(expected_values["id"]) + "/"

        # Run test
        set_user_auth_token(api_client, "Palpatine")
        with pytest.raises(answer_type.DoesNotExist):
            api_client.get(full_url)

    @pytest.mark.parametrize(
        "json_data",
        [
            pytest.param(
                dict(
                    question="1",
                    short_answer="Y",
                    justify_answer="Deserunt et velit ad occaecat qui.",
                ),
                id="YesNo [National Framework] answer",
            ),
            pytest.param(
                dict(
                    question="6",
                    short_answer="N",
                    justify_answer="Deserunt et velit ad occaecat qui.",
                ),
                id="YesNo [Key Agency Actions] answer",
            ),
            pytest.param(
                dict(question="3", selected_choice=str(EvolutionChoiceType.ENGAGED)),
                id="SingleChoice answer",
            ),
            pytest.param(
                dict(question="5", selected_programs=[2, 4]),
                id="MultipleChoice answer",
            ),
        ],
    )
    @pytest.mark.parametrize("epic_username", answer_fixture_users)
    def test_POST_answer(
        self,
        epic_username: str,
        json_data: dict,
        api_client: APIClient,
    ):
        def set_user(epic_username: str) -> int:
            epic_user: User = User.objects.filter(username=epic_username).first()
            if epic_user.is_staff or epic_user.is_superuser:
                json_data["user"] = User.objects.filter(username="Anakin").first().pk

        # Set test data.
        set_user_auth_token(api_client, epic_username)
        assert len(Answer.objects.all()) == 0  # No responses yet.
        set_user(epic_username)

        # Run request.
        response = api_client.post(self.url_root, json_data, format="json")
        assert response.status_code == 201
        assert len(Answer.objects.all()) == 1

    @pytest.mark.parametrize("epic_username", answer_fixture_users)
    @pytest.mark.parametrize("answer_type", get_submodel_type_list(Answer))
    def test_PATCH_answer(
        self,
        epic_username: str,
        answer_type: Type[Answer],
        api_client: APIClient,
        _answers_fixture: dict,
        _answers_update_fixture: dict,
    ):
        # Define test data
        expected_values = _answers_fixture[answer_type]
        answer_pk = str(expected_values["id"])
        full_url = self.url_root + answer_pk + "/"
        json_data = _answers_update_fixture[answer_type]

        # Verify initial expectations.
        answer_to_change = answer_type.objects.get(pk=answer_pk)
        assert answer_to_change is not None
        self._compare_answer_fields(answer_to_change, json_data, lambda x, y: x != y)

        # Run test
        set_user_auth_token(api_client, epic_username)
        response = api_client.patch(full_url, json_data, format="json")

        # Verify final expectations.
        assert response.status_code == 200
        changed_answer = answer_type.objects.get(pk=answer_pk)
        assert changed_answer is not None
        self._compare_answer_fields(changed_answer, json_data, lambda x, y: x == y)


@pytest.mark.django_db
class TestUrlUnavailableActions:
    @pytest.mark.parametrize(
        "url_root",
        [
            pytest.param(TestEpicUserTokenAuthRequest.url_root),
            pytest.param(TestEpicUserViewSet.url_root),
            pytest.param(TestAreaViewSet.url_root),
            pytest.param(TestAgencyViewSet.url_root),
            pytest.param(TestGroupViewSet.url_root),
            pytest.param(TestProgramViewSet.url_root),
            pytest.param(TestQuestionViewSet.url_root),
            pytest.param(TestAnswerViewSet.url_root),
        ],
    )
    def test_GET_without_auth_returns_error(self, url_root: str, api_client: APIClient):
        # Verify final exepctations.
        assert api_client.get(url_root).status_code in [403, 405]

    @pytest.mark.parametrize(
        "epic_username",
        [
            pytest.param(
                "Palpatine",
                id="Non admins user.",
            ),
            pytest.param(
                "admin",
                id="Admins user.",
            ),
        ],
    )
    @pytest.mark.parametrize(
        "url_root, data_dict",
        [
            pytest.param(TestAreaViewSet.url_root, {"name": "Area51"}),
            pytest.param(TestAgencyViewSet.url_root, {"name": "C.N.I."}),
            pytest.param(TestGroupViewSet.url_root, {"name": "NFG", "area": "1"}),
            pytest.param(TestProgramViewSet.url_root, {"name": "ACS", "group": "1"}),
        ],
    )
    def test_POST_with_auth_returns_error(
        self, url_root: str, data_dict: dict, epic_username: str, api_client: APIClient
    ):
        # Set test data
        set_user_auth_token(api_client, epic_username)

        # Run request.
        response = api_client.post(url_root, data_dict, format="json")

        # Verify final expectations. (Denied)
        assert response.status_code in [403, 405]

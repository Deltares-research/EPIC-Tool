import json
from typing import Callable, Optional, Type

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
from epic_app.models.epic_questions import (
    EvolutionChoiceType,
    EvolutionQuestion,
    KeyAgencyActionsQuestion,
    LinkagesQuestion,
    NationalFrameworkQuestion,
    Question,
)
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
    admin_user: User = User.objects.get(username="admin")
    assert admin_user.is_superuser
    assert admin_user.is_staff
    return admin_user


@pytest.mark.django_db
def get_epic_user(username: str) -> EpicUser:
    epic_user: EpicUser = EpicUser.objects.get(username=username)
    assert not epic_user.is_superuser
    assert not epic_user.is_staff
    return epic_user


@pytest.mark.django_db
def set_user_auth_token(api_client: APIClient, username: str) -> str:
    epic_user = User.objects.get(username=username)
    assert epic_user
    token_str = "Token " + epic_user.auth_token.key

    # Run request.
    api_client.credentials(HTTP_AUTHORIZATION=token_str)


@pytest.fixture
def admin_api_client(api_client: APIClient) -> APIClient:
    set_user_auth_token(api_client, "admin")
    return api_client


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
            pytest.param("", 405, id="GET"),
            pytest.param("2/", 404, id="RETRIEVE epic_user id=2"),
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

    anakin_json_data = {
        "url": "http://testserver/api/epicuser/3/",
        "id": 3,
        "username": "Anakin",
        "organization": 1,
        "selected_programs": [2, 4],
    }

    def test_GET_epic_user_as_admin(
        self,
        admin_api_client: APIClient,
    ):
        # Define test data.
        response = admin_api_client.get(self.url_root)

        # Verify final exepctations.
        assert response.status_code == 200
        assert len(response.data) > 1

    def test_GET_epic_user_as_user_not_allowed(
        self,
        api_client: APIClient,
    ):
        # Define test data.
        set_user_auth_token(api_client, "Palpatine")
        response = api_client.get(self.url_root)

        # Verify final exepctations.
        assert response.status_code == 403

    def test_RETRIEVE_epic_user_as_admin(
        self,
        admin_api_client: APIClient,
    ):
        # Define test data.
        user_found = get_epic_user("Anakin")
        url = f"{self.url_root}{user_found.pk}/"

        # Run request.
        response = admin_api_client.get(url)

        # Verify final exepctations.
        assert response.status_code == 200
        assert json.loads(response.content) == self.anakin_json_data

    @pytest.mark.parametrize("username", ["Anakin", "Palpatine"])
    def test_RETRIEVE_epic_user_as_user_not_allowed(
        self,
        username: str,
        api_client: APIClient,
    ):
        # Define test data.
        user_found = get_epic_user("Anakin")
        url = f"{self.url_root}{user_found.pk}/"

        # Run request.
        set_user_auth_token(api_client, username)
        response = api_client.get(url)

        # Verify final exepctations.
        assert response.status_code == 403

    @pytest.mark.parametrize(
        "epic_username",
        [
            pytest.param(None, id="No user authenticated"),
            pytest.param("Palpatine", id="Authenticated EpicUser"),
            pytest.param("admin", id="Admin User"),
        ],
    )
    def test_POST_not_allowed(self, epic_username: str, api_client: APIClient):
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

    @pytest.mark.parametrize(
        "epic_username, find_username, expected_response",
        [
            pytest.param(
                "Palpatine",
                "Anakin",
                dict(status_code=403, content={"detail": "Not found."}),
                id="Cannot update other users' password.",
            ),
            pytest.param(
                "Anakin",
                "Anakin",
                dict(status_code=200, content=anakin_json_data),
                id="Can update their own password.",
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
class TestEpicOrganizationViewSet:
    url_root = "/api/epicorganization/"

    @pytest.fixture(autouse=False)
    def admin_api_client(self, api_client: APIClient) -> APIClient:
        set_user_auth_token(api_client, "admin")
        return api_client

    @pytest.fixture(autouse=False)
    def _report_fixture(self) -> dict:
        def get_qa(question_id: int, answer_id: Optional[int]) -> dict:
            return dict(question=question_id, answer=answer_id)

        # Create some empty answers for 'Anakin'
        e_user = EpicUser.objects.get(username="Anakin")
        answers = []
        for nfq in NationalFrameworkQuestion.objects.all():
            # We will fill the answers for these ones.
            yna, _ = YesNoAnswer.objects.get_or_create(
                user=e_user, question=nfq, short_answer=YesNoAnswerType.YES
            )
            answers.append(get_qa(nfq.id, yna.id))
        for eq in EvolutionQuestion.objects.all():
            sca, _ = SingleChoiceAnswer.objects.get_or_create(user=e_user, question=eq)
            answers.append(get_qa(eq.id, sca.id))  # Empty answer
        for kaa in KeyAgencyActionsQuestion.objects.all():
            answers.append(get_qa(kaa.id, None))
        for lnk in LinkagesQuestion.objects.all():
            mca = MultipleChoiceAnswer(question=lnk, user=e_user)
            mca.save()
            mca.selected_programs.add(Program.objects.first(), Program.objects.last())
            answers.append(get_qa(lnk.id, mca.id))

        return None

    def test_GET_epic_organization_as_admin(self, admin_api_client: APIClient):
        # Run request
        response = admin_api_client.get(self.url_root)

        # Verify final expectations
        assert response.status_code == 200
        assert len(response.data) == len(EpicOrganization.objects.all())

    def test_GET_epic_organization_as_user_denied(self, api_client: APIClient):
        # Run request
        set_user_auth_token(api_client, "Anakin")
        response = api_client.get(self.url_root)

        # Verify final expectations
        assert response.status_code == 403

    def test_RETRIEVE_epic_organization_as_admin(self, admin_api_client: APIClient):
        # Run request
        response = admin_api_client.get(self.url_root + "1/")

        # Verify final expectations
        assert response.status_code == 200

    def test_RETRIEVE_epic_organization_as_user_denied(self, api_client: APIClient):
        # Run request
        set_user_auth_token(api_client, "Anakin")
        response = api_client.get(self.url_root + "1/")

        # Verify final expectations
        assert response.status_code == 403

    def test_RETRIEVE_report(self, _report_fixture: dict, admin_api_client: APIClient):
        full_url = self.url_root + "1/" + "report/"

        # Run request
        response = admin_api_client.get(full_url)

        # Verify final expectations
        assert response.status_code == 200
        assert len(response.data) == len(Program.objects.all())


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
            pytest.param("", 2, id="GET"),
            pytest.param("1/", 4, id="RETRIEVE (Area 'alpha' with 4 groups)"),
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
            pytest.param("", 4, id="GET"),
            pytest.param("1/", 4, id="RETRIEVE (Agency 'T.I.A.' with 4 fields)"),
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
            pytest.param("", 3, id="GET"),
            pytest.param("1/", 5, id="RETRIEVE (Group 'first' with 5 fields)"),
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
            pytest.param("", 5, id="GET"),
            pytest.param("1/", 7, id="RETRIEVE (Program 'a' with 9 fields)"),
        ],
    )
    def test_RETRIEVE_program(
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
                "question-nationalframework/", 2, id="NationalFramework Questions"
            ),
            pytest.param("question-evolution/", 2, id="Evolution Questions"),
            pytest.param("question-linkages/", 1, id="Linkages Questions"),
            pytest.param(
                "question-keyagencyactions/", 1, id="KeyAgencyActions Questions"
            ),
        ],
    )
    def test_GET_questions(
        self,
        url_suffix: str,
        expected_entries: int,
        api_client: APIClient,
    ):
        # Program 'a' has 6 questions (2xNFQ, 2xEVO, 1xKA, 1xLNK)
        a_program: Program = Program.objects.get(name="a")
        full_url = self.url_root + f"{a_program.pk}/" + url_suffix
        # Run request.
        set_user_auth_token(api_client, "Palpatine")
        response = api_client.get(full_url)

        # Verify final exepctations.
        assert response.status_code == 200
        assert len(response.data) == expected_entries

    @pytest.fixture(autouse=False)
    def _progress_fixture(self) -> dict:
        def get_qa(question_id: int, answer_id: Optional[int]) -> dict:
            return dict(question=question_id, answer=answer_id)

        # Create some empty answers for 'Anakin'
        e_user = EpicUser.objects.get(username="Anakin")
        answers = []
        for nfq in NationalFrameworkQuestion.objects.all():
            # We will fill the answers for these ones.
            yna, _ = YesNoAnswer.objects.get_or_create(
                user=e_user, question=nfq, short_answer=YesNoAnswerType.YES
            )
            answers.append(get_qa(nfq.id, yna.id))
        for eq in EvolutionQuestion.objects.all():
            sca, _ = SingleChoiceAnswer.objects.get_or_create(user=e_user, question=eq)
            answers.append(get_qa(eq.id, sca.id))  # Empty answer
        for kaa in KeyAgencyActionsQuestion.objects.all():
            answers.append(get_qa(kaa.id, None))
        for lnk in LinkagesQuestion.objects.all():
            answers.append(get_qa(lnk.id, None))

        return {
            "progress": len(NationalFrameworkQuestion.objects.all()) / len(answers),
            "questions_answers": answers,
        }

    def test_RETRIEVE_progress_epic_user(
        self, api_client: APIClient, _progress_fixture: dict
    ):
        # Define test data.
        # Program 'a' has 6 questions (2xNFQ, 2xEVO, 2xKAA 1xLNK)
        progress_suffix = "progress/"
        progress_fixture_user = "Anakin"
        a_program: Program = Program.objects.get(name="a")
        full_url = self.url_root + f"{a_program.pk}/" + progress_suffix

        # Run request.
        set_user_auth_token(api_client, progress_fixture_user)
        response = api_client.get(full_url)

        # Verify final expectations
        assert response.status_code == 200
        assert len(response.data) == 2
        assert len(response.data["questions_answers"]) == 6  # 'a' has 6 questions.
        assert list(response.data.keys()) == list(_progress_fixture.keys())
        assert response.data["progress"] == _progress_fixture["progress"]
        assert len(response.data["questions_answers"]) == len(
            _progress_fixture["questions_answers"]
        )
        for qa in response.data["questions_answers"]:
            assert qa in _progress_fixture["questions_answers"]


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
            if answer_field == "user":
                assert str(a_instance.user.id) == str(answer_value)
            elif answer_field == "question":
                assert str(a_instance.question.id) == str(answer_value)
            else:
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

    update_patch_params = [
        pytest.param(
            {
                YesNoAnswer: dict(
                    short_answer="",
                ),
                SingleChoiceAnswer: dict(
                    selected_choice="",
                ),
                MultipleChoiceAnswer: dict(selected_programs=[]),
            },
            id="Set values to empty",
        ),
        pytest.param(
            {
                YesNoAnswer: dict(
                    short_answer=str(YesNoAnswerType.YES),
                    justify_answer="For my own reasons",
                ),
                SingleChoiceAnswer: dict(
                    selected_choice=str(EvolutionChoiceType.ENGAGED),
                    justify_answer="For the lulz",
                ),
                MultipleChoiceAnswer: dict(selected_programs=[3, 4]),
            },
            id="Set new values",
        ),
    ]

    answer_fixture_users = [
        pytest.param("Anakin", id="Instance owner"),
        pytest.param("Palpatine", id="Non-instance owner authenticated user"),
        pytest.param("admin", id="Admin (super_user / staff)"),
    ]

    @pytest.mark.parametrize("username", answer_fixture_users)
    def test_GET_answer_returns_only_users_answers(
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
        if not username == self.anakin.username:
            assert len(response.data) == 0
            return
        assert len(response.data) == 3
        assert json.dumps(response.data) == json.dumps(expected_values)

    @pytest.mark.parametrize("username", answer_fixture_users)
    @pytest.mark.parametrize("answer_type", get_submodel_type_list(Answer))
    def test_RETRIEVE_answer_only_for_instance_owner(
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
        if username == "Anakin":
            assert response.status_code == 200
            assert response.data == expected_values
        else:
            assert response.status_code == 403

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
    @pytest.mark.parametrize("update_dict", update_patch_params)
    def test_PATCH_answer(
        self,
        epic_username: str,
        answer_type: Type[Answer],
        update_dict: dict,
        api_client: APIClient,
        _answers_fixture: dict,
    ):
        # Define test data
        expected_values = _answers_fixture[answer_type]
        answer_pk = str(expected_values["id"])
        full_url = self.url_root + answer_pk + "/"
        json_data = update_dict[answer_type]

        # Verify initial expectations.
        answer_to_change = answer_type.objects.get(pk=answer_pk)
        assert answer_to_change is not None
        self._compare_answer_fields(answer_to_change, json_data, lambda x, y: x != y)

        # Run test
        set_user_auth_token(api_client, epic_username)
        response = api_client.patch(full_url, json_data, format="json")

        # Verify final expectations.
        if not epic_username == "Anakin":
            assert response.status_code == 404
            return
        assert response.status_code == 200
        changed_answer = answer_type.objects.get(pk=answer_pk)
        assert changed_answer is not None
        self._compare_answer_fields(changed_answer, json_data, lambda x, y: x == y)

    @pytest.mark.parametrize("epic_username", answer_fixture_users)
    @pytest.mark.parametrize("answer_type", get_submodel_type_list(Answer))
    @pytest.mark.parametrize("update_dict", update_patch_params)
    def test_PUT_answer(
        self,
        epic_username: str,
        answer_type: Type[Answer],
        update_dict: dict,
        api_client: APIClient,
        _answers_fixture: dict,
    ):
        # Define test data
        expected_values = _answers_fixture[answer_type]
        answer_pk = str(expected_values["id"])
        full_url = self.url_root + answer_pk + "/"
        json_data = update_dict[answer_type]

        # Verify initial expectations.
        answer_to_change: Answer = answer_type.objects.get(pk=answer_pk)
        assert answer_to_change is not None
        # Data needs to be extended with user, and question.
        json_data["user"] = answer_to_change.user.id
        json_data["question"] = answer_to_change.question.id
        self._compare_answer_fields(answer_to_change, json_data, lambda x, y: x != y)

        # Run test
        set_user_auth_token(api_client, epic_username)
        response = api_client.put(full_url, json_data, format="json")

        # Verify final expectations.
        if not epic_username == "Anakin":
            assert response.status_code == 404
            return
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
            pytest.param(TestEpicOrganizationViewSet.url_root),
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
            pytest.param(
                TestEpicOrganizationViewSet.url_root,
                {"name": "Riot"},
                id="EpicOrganization",
            ),
            pytest.param(
                TestEpicUserViewSet.url_root,
                {"username": "ClarkKent", "password": "!amSup3rm4n"},
                id="EpicUser",
            ),
            pytest.param(TestAreaViewSet.url_root, {"name": "Area51"}, id="Area"),
            pytest.param(TestAgencyViewSet.url_root, {"name": "C.N.I."}, id="Agency"),
            pytest.param(
                TestGroupViewSet.url_root, {"name": "NFG", "area": "1"}, id="Group"
            ),
            pytest.param(
                TestProgramViewSet.url_root, {"name": "ACS", "group": "1"}, id="Program"
            ),
            pytest.param(
                TestQuestionViewSet.url_root,
                {"title": "A dummy question", "program": "1"},
                id="Question",
            ),
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

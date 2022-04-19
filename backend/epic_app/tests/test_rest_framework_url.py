import json

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
from epic_app.models.epic_user import EpicUser
from epic_app.models.models import Program
from epic_app.tests.epic_db_fixture import epic_test_db


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
        "organization": "Gallactic Empire",
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
            "organization": "Daily Planet",
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
class TestQuestionsViewSet:
    nfq_url = "/api/nationalframeworkquestion/"
    evo_url = "/api/evolutionquestion/"
    lnk_url = "/api/linkagesquestion/"

    @pytest.mark.parametrize(
        "epic_username",
        [
            pytest.param(
                "Palpatine",
                id="Non admin user with the selected programs.",
            ),
            pytest.param("Anakin", id="Non admin user without the selected programs."),
            pytest.param(
                "admin",
                id="Admins user.",
            ),
        ],
    )
    @pytest.mark.parametrize(
        "question_url, expected_entries",
        [
            pytest.param(nfq_url, 2, id="list Nationalframework question"),
            pytest.param(evo_url, 2, id="list Evolution question"),
            pytest.param(lnk_url, 1, id="list Linkages question"),
            pytest.param(nfq_url + "1/", 4, id="retrieve (NFQ 'a' with 7 fields)"),
            pytest.param(evo_url + "3/", 4, id="retrieve (EVO 'a' with 7 fields)"),
            pytest.param(lnk_url + "5/", 3, id="retrieve (LNK 'a' with 7 fields)"),
        ],
    )
    def test_GET_question(
        self,
        epic_username: str,
        question_url: str,
        expected_entries: int,
        api_client: APIClient,
    ):
        # Run request.
        set_user_auth_token(api_client, epic_username)
        response = api_client.get(question_url)

        # Verify final exepctations.
        assert response.status_code == 200
        assert len(response.data) == expected_entries


@pytest.mark.django_db
class TestAnswerViewSet:
    yesno_url = "/api/yesnoanswer/"
    singlechoice_url = "/api/singleanswer/"
    multiplechoice_url = "/api/multianswer/"

    @pytest.fixture
    def anakin_answers_fixture(self):
        anakin = EpicUser.objects.filter(username="Anakin").first()
        YesNoAnswer.objects.create(
            user=anakin,
            question=Question.objects.filter(pk=1).first(),
            short_answer=YesNoAnswerType.NO,
            justify_answer="Laboris proident enim dolore ullamco voluptate nisi labore laborum ut qui adipisicing occaecat exercitation culpa.",
        )
        SingleChoiceAnswer.objects.create(
            user=anakin,
            question=Question.objects.filter(pk=3).first(),
            selected_choice=EvolutionChoiceType.EFFECTIVE,
            justify_answer="Ea ut ipsum deserunt culpa laborum excepteur laboris ad adipisicing ad officia laboris.",
        )
        mca = MultipleChoiceAnswer(
            user=anakin,
            question=Question.objects.filter(pk=5).first(),
        )
        mca.save()
        mca.selected_programs.add(4, 2)

    @pytest.mark.parametrize(
        "answer_url",
        [
            pytest.param(yesno_url, id="Yes-No Answer"),
            pytest.param(singlechoice_url, id="Singlechoice Answer"),
            pytest.param(multiplechoice_url, id="Multiplechoice Answer"),
        ],
    )
    @pytest.mark.parametrize(
        "epic_username, expected_response",
        [
            pytest.param(
                "Palpatine",
                dict(response=200, entries=0),
                id="Non admin user cannot GET-LIST other user's answers.",
            ),
            pytest.param(
                "Anakin",
                dict(response=200, entries=1),
                id="Non admin user can GET-LIST his answers.",
            ),
            pytest.param(
                "admin",
                dict(response=200, entries=1),
                id="Admin user can GET-LIST all answers.",
            ),
        ],
    )
    def test_GET_LIST_answer(
        self,
        answer_url: str,
        epic_username: str,
        expected_response: dict,
        anakin_answers_fixture,
        api_client: APIClient,
    ):
        # Run request.
        set_user_auth_token(api_client, epic_username)
        response = api_client.get(answer_url)

        # Verify final expectations
        assert response.status_code == expected_response["response"]
        if response.status_code == 200:
            assert len(response.data) == expected_response["entries"]

    yesno_anakin = {
        "url": "http://testserver/api/yesnoanswer/1/",
        "id": 1,
        "user": 3,
        "question": 1,
        "short_answer": "N",
        "justify_answer": "Laboris proident enim dolore ullamco voluptate nisi labore laborum ut qui adipisicing occaecat exercitation culpa.",
    }

    singlechoice_anakin = {
        "url": "http://testserver/api/singleanswer/2/",
        "id": 2,
        "user": 3,
        "question": 3,
        "selected_choice": "Effective",
        "justify_answer": "Ea ut ipsum deserunt culpa laborum excepteur laboris ad adipisicing ad officia laboris.",
    }
    multiplechoice_anakin = {
        "id": 3,
        "question": 5,
        "selected_programs": [2, 4],
        "url": "http://testserver/api/multianswer/3/",
        "user": 3,
    }

    @pytest.mark.parametrize(
        "epic_username, expected_code",
        [
            pytest.param(
                "Anakin",
                200,
                id="Non admin user can RETRIEVE his answer.",
            ),
            pytest.param(
                "Palpatine",
                404,
                id="Non admin user cannot RETRIEVE other user's answer.",
            ),
            pytest.param(
                "admin",
                200,
                id="Admin user can ANY answers.",
            ),
        ],
    )
    @pytest.mark.parametrize(
        "answer_url, expected_data",
        [
            pytest.param(
                yesno_url + "1/",
                yesno_anakin,
                id="Yes-No Answer",
            ),
            pytest.param(
                singlechoice_url + "2/",
                singlechoice_anakin,
                id="Singlechoice Answer",
            ),
            pytest.param(
                multiplechoice_url + "3/",
                multiplechoice_anakin,
                id="Multiplechoice Answer",
            ),
        ],
    )
    def test_GET_DETAIL_answer(
        self,
        answer_url: str,
        epic_username: str,
        expected_code: int,
        expected_data: dict,
        anakin_answers_fixture,
        api_client: APIClient,
    ):
        # Run request.
        set_user_auth_token(api_client, epic_username)
        response = api_client.get(answer_url)

        # Verify final expectations
        assert response.status_code == expected_code
        if response.status_code == 200:
            assert json.loads(response.content) == expected_data

    @pytest.mark.parametrize(
        "answer_url, json_data",
        [
            pytest.param(
                yesno_url,
                dict(
                    question="1",
                    short_answer="Y",
                    justify_answer="Deserunt et velit ad occaecat qui.",
                ),
                id="YesNo answer",
            ),
            pytest.param(
                singlechoice_url,
                dict(question="3", selected_choice="ENGAGED"),
                id="SingleChoice answer",
            ),
            pytest.param(
                multiplechoice_url,
                dict(question="5", selected_programs="[2,4]"),
                id="MultipleChoice answer",
            ),
        ],
    )
    @pytest.mark.parametrize(
        "epic_username",
        [pytest.param("Anakin", id="Non-admin"), pytest.param("admin", id="Admin")],
    )
    def test_POST_answer(
        self,
        answer_url: str,
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
        response = api_client.post(answer_url, json_data, format="json")
        assert response.status_code == 201
        assert len(Answer.objects.all()) == 1


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
            pytest.param(TestQuestionsViewSet.nfq_url),
            pytest.param(TestQuestionsViewSet.evo_url),
            pytest.param(TestQuestionsViewSet.lnk_url),
            pytest.param(TestAnswerViewSet.yesno_url),
            pytest.param(TestAnswerViewSet.singlechoice_url),
            pytest.param(TestAnswerViewSet.multiplechoice_url),
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

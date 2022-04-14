import json
from tokenize import Token

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from epic_app.models.epic_user import EpicUser
from epic_app.models.models import Area
from epic_app.tests.epic_db_fixture import epic_test_db


@pytest.fixture(autouse=True)
def rest_framework_url_fixture(epic_test_db: pytest.fixture):
    """
    Dummy fixture just to load a default db from dummy_db.

    Args:
        epic_test_db (pytest.fixture): Fixture to load for the whole file tests.
    """
    pass
    # # Create a dummy user that we can safely invoke from the rest of this test file.
    # waldo = EpicUser(username="Waldo", organization="World Bank")
    # waldo.set_password("iamwaldo")
    # waldo.save()


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

    @pytest.mark.parametrize(
        "epic_username, find_username, expected_code",
        [
            pytest.param(
                "Palpatine",
                "Anakin",
                404,
                id="Non admins cannot retrieve other users.",
            ),
            pytest.param(
                "Anakin",
                "Anakin",
                200,
                id="Non admins can retrieve themselves.",
            ),
            pytest.param(
                "admin",
                "Anakin",
                200,
                id="Admins can retrieve other users.",
            ),
        ],
    )
    def test_GET_detail_epic_user(
        self,
        epic_username: str,
        find_username: str,
        expected_code: int,
        api_client: APIClient,
    ):
        # Define test data.
        user_found = get_epic_user(find_username)
        url = f"{self.url_root}{user_found.pk}/"

        # Run request.
        set_user_auth_token(api_client, epic_username)
        response = api_client.get(url)

        # Verify final exepctations.
        assert response.status_code == expected_code


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
            pytest.param("1/", 4, id="get-retrieve (Area 1 with 4 groups)"),
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


@pytest.mark.django_db
class TestGroupViewSet:
    url_root = "/api/group/"


@pytest.mark.django_db
class TestProgramViewSet:
    url_root = "/api/program/"


@pytest.mark.django_db
class TestAnswerViewSet:
    url_root = "/api/answer/"


@pytest.mark.django_db
class TestUrlWithoutAuth:
    @pytest.mark.parametrize(
        "api_call", [pytest.param(lambda x, y: x.get(y), id="GET")]
    )
    @pytest.mark.parametrize(
        "url_root",
        [
            pytest.param(TestEpicUserViewSet.url_root),
            pytest.param(TestAreaViewSet.url_root),
            pytest.param(TestAgencyViewSet.url_root),
            pytest.param(TestGroupViewSet.url_root),
            pytest.param(TestProgramViewSet.url_root),
            pytest.param(TestAnswerViewSet.url_root),
        ],
    )
    def test_given_api_call_without_auth_returns_error(
        self, api_call, url_root: str, api_client: APIClient
    ):
        # Verify final exepctations.
        assert api_call(api_client, url_root).status_code == 403

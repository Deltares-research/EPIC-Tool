import json
from tokenize import Token

import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.response import Response as RfResponse
from rest_framework.test import APIClient, APIRequestFactory

from epic_app.models.epic_user import EpicUser
from epic_app.tests.epic_db_fixture import epic_test_db
from epic_app.views import EpicUserViewSet


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


class UrlExpectedResult:
    status_code: int
    result_data: dict


class UrlTestCase:
    epic_user: EpicUser
    expected_result: UrlExpectedResult


@pytest.mark.django_db
class TestEpicUserViewSet:
    url_root = "/api/epicuser/"

    def _get_admin_user(self) -> User:
        admin_user: User = User.objects.filter(username="admin").first()
        assert admin_user.is_superuser
        assert admin_user.is_staff
        return admin_user

    def _get_epic_user(self, username: str) -> EpicUser:
        epic_user: EpicUser = EpicUser.objects.filter(username=username).first()
        assert not epic_user.is_superuser
        assert not epic_user.is_staff
        return epic_user

    def test_GET_list_epicuser_when_user_is_admin(self):
        # Define test data.
        url = "api/epicuser/"

        # Run request.
        factory = APIRequestFactory()
        request = factory.get(url)
        request.user = self._get_admin_user()
        response: RfResponse = EpicUserViewSet.as_view({"get": "list"})(request)

        # Verify final exepctations.
        assert response.status_code == 200
        assert len(response.data) >= 2  # Anakin + Palpatine

    def test_GET_list_epicuser_when_user_is_not_admin(self):
        # Define test data.
        url = "api/epicuser/"

        # Run request.
        factory = APIRequestFactory()
        request = factory.get(url)
        request.user = self._get_epic_user()
        response: RfResponse = EpicUserViewSet.as_view({"get": "list"})(request)

        # Verify final exepctations.
        assert response.status_code == 200
        assert len(response.data) == 1

    # def test_GET_detail_epicuser_when_user_is_admin(self, api_client: APIClient):
    #     # Define test data.
    #     id_to_find = self._get_epic_user("Anakin").pk
    #     url = f"{self.url_root}{id_to_find}/"
    #     # Run request.
    #     api_client.force_authenticate(user=self._get_admin_user())
    #     response = api_client.get(url)

    #     # Verify final exepctations.
    #     assert response.status_code == 200
    #     assert response.data

    # def test_GET_api_detail_epicuser_given_user(
    #     self,
    #     api_client: APIClient,
    # ):
    #     # Define test data.
    #     anakin_user = self._get_epic_user("Anakin")
    #     url = f"{self.url_root}{anakin_user.pk}/"
    #     token_str = "Token " + anakin_user.auth_token.key

    #     # Run request.
    #     client: APIClient = api_client()
    #     client.credentials(HTTP_AUTHORIZATION=token_str)
    #     response = client.get(url)

    #     # Verify final exepctations.
    #     assert response.status_code == 200
    #     assert response.data

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
        user_found = self._get_epic_user(find_username)
        url = f"{self.url_root}{user_found.pk}/"

        epic_user = User.objects.filter(username=epic_username).first()
        assert epic_user
        token_str = "Token " + epic_user.auth_token.key

        # Run request.
        api_client.credentials(HTTP_AUTHORIZATION=token_str)
        response = api_client.get(url)

        # Verify final exepctations.
        assert response.status_code == expected_code


class TestAreaViewSet:
    pass


class TestAgencyViewSet:
    pass


class TestGroupoViewSet:
    pass


class TestProgramViewSet:
    pass


class TestAnswerViewSet:
    pass

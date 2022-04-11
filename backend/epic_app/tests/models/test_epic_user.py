import json

import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.response import Response as RfResponse
from rest_framework.test import APIRequestFactory

from epic_app.models.epic_user import EpicUser
from epic_app.tests.epic_db_fixture import epic_test_db
from epic_app.views import EpicUserViewSet


@pytest.fixture(autouse=True)
def epic_user_fixture(epic_test_db: pytest.fixture):
    """
    Dummy fixture just to load a default db from dummy_db.

    Args:
        epic_test_db (pytest.fixture): Fixture to load for the whole file tests.
    """
    # Create a dummy user that we can safely invoke from the rest of this test file.
    waldo = EpicUser(username="Waldo", organization="World Bank")
    waldo.set_password("iamwaldo")
    waldo.save()


def get_waldo() -> EpicUser:
    """
    Gets the EpicUser 'Waldo' to keep the code DRY.

    Returns:
        EpicUser: Dummy user created for the 'EpicUser' test-fixture.
    """
    waldo_user = EpicUser.objects.filter(username="Waldo").first()
    assert isinstance(waldo_user, EpicUser)
    assert len(waldo_user.selected_programs) == 0
    return waldo_user


@pytest.mark.django_db
class TestEpicUser:
    def test_init_epicuser(self):
        created_user = EpicUser.objects.create(
            username="Luke", organization="Rebel Alliance"
        )
        assert isinstance(created_user, EpicUser)
        assert isinstance(created_user, User)
        assert created_user.is_superuser is False
        assert not any(created_user.selected_programs.all())


@pytest.mark.django_db
class TestEpicUserTokenAuthRequest:
    def test_POST_valid_username_password_to_token_auth_succeeds(self):
        # Set test data
        eu_name: str = "Waldo"
        eu_pass: str = "iamwaldo"
        url = "api/token-auth"
        data = {"username": eu_name, "password": eu_pass}

        # Run request.
        factory = APIRequestFactory()
        request = factory.post(url, json.dumps(data), content_type="application/json")
        response: RfResponse = obtain_auth_token(request)

        # Verify final expectations.
        assert response.status_code == 200
        assert response.data.get("token") is not None

    def test_POST_wrong_username_password_to_token_auth_fails(self):
        # Set test data
        eu_name: str = "Waldo"
        eu_pass: str = "not_the_pass"
        url = "api/token-auth"
        data = {"username": eu_name, "password": eu_pass}

        # Run request.
        factory = APIRequestFactory()
        request = factory.post(url, json.dumps(data), content_type="application/json")
        response: RfResponse = obtain_auth_token(request)

        # Verify final expectations.
        assert response.status_code == 400
        assert response.data.get("token") is None


@pytest.mark.django_db
class TestEpicUser:
    def test_GET_epicuser_when_user_is_admin(self):
        # Define test data.
        url = "api/epicuser/"
        admin_user: User = User.objects.filter(username="admin").first()
        assert admin_user.is_superuser is True
        assert admin_user.is_staff is True
        # Run request.
        factory = APIRequestFactory()
        request = factory.get(url)
        request.user = admin_user
        response: RfResponse = EpicUserViewSet.as_view({"get": "list"})(request)

        # Verify final exepctations.
        assert response.status_code == 200
        assert len(response.data) >= 3

    def test_GET_epicuser_when_user_is_not_admin(self):
        # Define test data.
        url = "api/epicuser/"
        found_user: User = EpicUser.objects.filter(username="Anakin").first()
        assert found_user.is_superuser is False
        assert found_user.is_staff is False
        # Run request.
        factory = APIRequestFactory()
        request = factory.get(url)
        request.user = found_user
        response: RfResponse = EpicUserViewSet.as_view({"get": "list"})(request)

        # Verify final exepctations.
        assert response.status_code == 200
        assert len(response.data) == 1

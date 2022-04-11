import json

import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.response import Response as RfResponse
from rest_framework.test import APIRequestFactory

from epic_app.models.epic_user import EpicUser
from epic_app.tests.epic_db_fixture import epic_test_db


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
class TestEpicUserRequest:
    def test_POST_valid_username_password_to_token_auth_succeeds(self):
        # Set test data
        eu_name: str = "Waldo"
        eu_pass: str = "iamwaldo"
        url = "api/token-auth"
        data = {"username": eu_name, "password": eu_pass}

        # Either the url is not being picke up (test config probably).
        # Or the password is not correct.
        factory = APIRequestFactory()
        request = factory.post(url, json.dumps(data), content_type="application/json")
        response: RfResponse = obtain_auth_token(request)
        assert response.status_code == 200
        assert response.data.get("token") is not None

    def test_POST_wrong_username_password_to_token_auth_fails(self):
        # Set test data
        eu_name: str = "Waldo"
        eu_pass: str = "not_the_pass"
        url = "api/token-auth"
        data = {"username": eu_name, "password": eu_pass}

        # Either the url is not being picke up (test config probably).
        # Or the password is not correct.
        factory = APIRequestFactory()
        request = factory.post(url, json.dumps(data), content_type="application/json")
        response: RfResponse = obtain_auth_token(request)
        assert response.status_code == 400
        assert response.data.get("token") is None

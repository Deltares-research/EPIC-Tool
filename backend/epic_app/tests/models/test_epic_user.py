import json

import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.response import Response as RfResponse
from rest_framework.test import APIRequestFactory

from epic_app.models.epic_user import EpicOrganization, EpicUser
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
    world_bank = EpicOrganization.objects.create(name="World Bank")
    waldo = EpicUser(username="Waldo", organization=world_bank)
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
    return waldo_user


@pytest.mark.django_db
class TestEpicOrganization:
    def test_init_epicorganization(self):
        created_org = EpicOrganization.objects.create(name="random")
        assert isinstance(created_org, EpicOrganization)
        assert (
            len(created_org.organization_users.all()) == 0
        )  # Related field from EpicUser foreign key.

    def test_generate_users(self):
        last_org: EpicOrganization = EpicOrganization.objects.last()
        previous_users = len(EpicUser.objects.all())
        new_users = last_org.generate_users(24)
        assert all(isinstance(nu, EpicUser) for nu in new_users)
        assert all(nu.organization == last_org for nu in new_users)
        assert all(last_org.organization_users.contains(n_user) for n_user in new_users)
        assert len(EpicUser.objects.all()) - len(new_users) == previous_users


@pytest.mark.django_db
class TestEpicUser:
    def test_init_epicuser(self):
        epic_organization = EpicOrganization.objects.last()
        created_user = EpicUser.objects.create(
            username="Luke", organization=epic_organization
        )
        assert isinstance(created_user, EpicUser)
        assert isinstance(created_user, User)
        assert created_user.is_superuser is False
        assert created_user.is_staff is False
        assert created_user.is_advisor is False
        assert created_user in epic_organization.organization_users.all()
        assert Token.objects.filter(user=created_user).exists()


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

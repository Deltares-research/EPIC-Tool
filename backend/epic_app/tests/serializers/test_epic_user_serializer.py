from typing import List

import pytest
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from epic_app.models.epic_user import EpicOrganization, EpicUser
from epic_app.serializers.epic_user_serializer import (
    EpicOrganizationSerializer,
    EpicUserSerializer,
)
from epic_app.tests.epic_db_fixture import epic_test_db


@pytest.fixture(autouse=True)
@pytest.mark.django_db
def epic_user_serializer_fixture(
    epic_test_db: pytest.fixture,
):
    """
    Dummy fixture just to load a default db from dummy_db.

    Args:
        epic_test_db (pytest.fixture): Fixture to load for the whole file tests.
    """
    pass


def get_serializer():
    factory = APIRequestFactory()
    request = factory.get("/")

    return {
        "request": Request(request),
    }


serializer_context = get_serializer()


@pytest.mark.django_db
class TestEpicUserSerializer:
    def test_given_valid_instances_returns_expected_data(self):
        # Define context
        serialized_data = list(
            EpicUserSerializer(
                EpicUser.objects.all(), many=True, context=serializer_context
            ).data
        )
        assert len(serialized_data) == 3

        def validate_epic_user_dict(
            epic_user_dict: dict,
            e_user: str,
            is_advisor: bool,
        ):
            assert isinstance(epic_user_dict, dict)
            assert epic_user_dict["username"] == e_user
            assert epic_user_dict["organization"] == 1
            assert epic_user_dict["is_advisor"] == is_advisor

        validate_epic_user_dict(serialized_data[0], "Palpatine", False)
        validate_epic_user_dict(serialized_data[1], "Anakin", False)
        validate_epic_user_dict(serialized_data[2], "Dooku", True)


@pytest.mark.django_db
class TestEpicOrganizationSerializer:
    def test_given_valid_instances_returns_expected_data(self):
        # Define context
        serialized_data = list(
            EpicOrganizationSerializer(
                EpicOrganization.objects.all(), many=True, context=serializer_context
            ).data
        )
        expected_data = {
            "url": "http://testserver/api/epicorganization/1/",
            "name": "Gallactic Empire",
            "organization_users": [2, 3, 4],
        }
        assert len(serialized_data) == 1
        assert serialized_data[0] == expected_data

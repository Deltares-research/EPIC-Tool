import pytest
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from epic_app.tests.epic_db_fixture import epic_test_db


@pytest.fixture(autouse=True)
def answer_serializer_fixture(
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


@pytest.mark.djangodb
class TestAnswerSerializer:
    pass

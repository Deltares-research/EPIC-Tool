import pytest

from epic_app.models.epic_questions import Question
from epic_app.tests.epic_db_fixture import epic_test_db


@pytest.fixture(autouse=True)
def QuestionSerializerFixture(epic_test_db: pytest.fixture):
    """
    Dummy fixture just to load a default db from dummy_db.

    Args:
        epic_test_db (pytest.fixture): Fixture to load for the whole file tests.
    """
    pass


@pytest.mark.django_db
class TestQuestionSerializer:
    def test_question_serializer_shows_valid_data(self):
        pass

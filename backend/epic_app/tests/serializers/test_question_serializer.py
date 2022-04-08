from typing import Dict, OrderedDict, Tuple

import pytest

from epic_app.models.epic_questions import (
    EvolutionQuestion,
    LinkagesQuestion,
    NationalFrameworkQuestion,
    Question,
)
from epic_app.models.models import Program
from epic_app.serializers.question_serializer import (
    EvolutionQuestionSerializer,
    LinkagesQuestionSerializer,
    NationalFrameworkQuestionSerializer,
    QuestionSerializer,
)
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
    def test_given_valid_instances_when_to_representation_returns_expected_data(self):
        def validate_fields(dict_item: dict) -> bool:
            valid_fields = ["title", "program", "id"]
            return all(d_key in valid_fields for d_key in dict_item.keys())

        serialized_data = list(
            QuestionSerializer(Question.objects.all(), many=True).data
        )

        assert len(serialized_data) == 4
        assert all(map(validate_fields, serialized_data))


@pytest.mark.django_db
class TestNationalFrameworkSerializer:
    def test_given_valid_instances_when_to_representation_returns_expected_data(self):
        def validate_fields(dict_item: dict) -> bool:
            valid_fields = ["title", "program", "id", "description"]
            return all(d_key in valid_fields for d_key in dict_item.keys())

        serialized_data = list(
            NationalFrameworkQuestionSerializer(
                NationalFrameworkQuestion.objects.all(), many=True
            ).data
        )

        assert len(serialized_data) == 2
        assert all(map(validate_fields, serialized_data))


@pytest.mark.django_db
class TestEvolutionQuestionSerializer:
    def test_given_valid_instances_when_to_representation_returns_expected_data(self):
        def validate_fields(dict_item: dict) -> bool:
            valid_fields = [
                "title",
                "program",
                "id",
                "nascent_description",
                "engaged_description",
                "capable_description",
                "effective_description",
            ]
            return all(d_key in valid_fields for d_key in dict_item.keys())

        serialized_data = list(
            EvolutionQuestionSerializer(EvolutionQuestion.objects.all(), many=True).data
        )

        assert len(serialized_data) == 2
        assert all(map(validate_fields, serialized_data))


@pytest.mark.django_db
class TestLinkagesQuestionSerializer:
    def test_given_valid_instances_when_to_representation_returns_expected_data(self):
        def validate_fields(dict_item: dict) -> bool:
            valid_fields = ["title", "program", "id"]
            return all(d_key in valid_fields for d_key in dict_item.keys())

        serialized_data = list(
            LinkagesQuestionSerializer(LinkagesQuestion.objects.all(), many=True).data
        )

        assert len(serialized_data) == 1
        assert all(map(validate_fields, serialized_data))

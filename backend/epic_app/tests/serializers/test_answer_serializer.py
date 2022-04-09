import pytest
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from epic_app.models.epic_questions import (
    Answer,
    EvolutionChoiceType,
    EvolutionQuestion,
    LinkagesQuestion,
    MultipleChoiceAnswer,
    NationalFrameworkQuestion,
    Question,
    SingleChoiceAnswer,
    YesNoAnswer,
    YesNoAnswerType,
)
from epic_app.models.models import EpicUser, Program
from epic_app.serializers.answer_serializer import AnswerSerializer
from epic_app.tests.epic_db_fixture import epic_test_db


@pytest.fixture(autouse=True)
@pytest.mark.django_db
def answer_serializer_fixture(
    epic_test_db: pytest.fixture,
):
    """
    Dummy fixture just to load a default db from dummy_db.

    Args:
        epic_test_db (pytest.fixture): Fixture to load for the whole file tests.
    """
    theonewhoasks = EpicUser.objects.create(
        username="TheOneWhoAsks", organization="TestCorp"
    )
    nf_answer: YesNoAnswer = NationalFrameworkQuestion.objects.first().get_answer(
        q_user=theonewhoasks
    )
    nf_answer.short_answer = YesNoAnswerType.YES
    nf_answer.justify_answer = "Because reasons."
    eq_answer: SingleChoiceAnswer = EvolutionQuestion.objects.first().get_answer(
        q_user=theonewhoasks
    )
    eq_answer.selected_choice = EvolutionChoiceType.CAPABLE
    eq_answer.justify_answer = "Because other reasons."
    lq_answer: MultipleChoiceAnswer = LinkagesQuestion.objects.first().get_answer(
        q_user=theonewhoasks
    )
    [lq_answer.selected_programs.add(p.id) for p in Program.objects.all()[1:4]]


def get_serializer():
    factory = APIRequestFactory()
    request = factory.get("/")

    return {
        "request": Request(request),
    }


serializer_context = get_serializer()


@pytest.mark.django_db
class TestAnswerSerializer:
    def test_given_valid_instances_when_to_representation_returns_expected_data(self):
        # Define context
        serialized_data = list(
            AnswerSerializer(
                Answer.objects.all(), many=True, context=serializer_context
            ).data
        )

        assert len(serialized_data) == 3

        def validate_concrete_questions(
            serialized_dict, nf_answer: bool, ev_answer: bool, lk_answer: bool
        ) -> bool:
            assert isinstance(serialized_dict["yesnoanswer"], dict) == nf_answer
            assert isinstance(serialized_dict["singlechoiceanswer"], dict) == ev_answer
            assert (
                isinstance(serialized_dict["multiplechoiceanswer"], dict) == lk_answer
            )

        validate_concrete_questions(serialized_data[0], True, False, False)
        validate_concrete_questions(serialized_data[1], False, True, False)
        validate_concrete_questions(serialized_data[2], False, False, True)

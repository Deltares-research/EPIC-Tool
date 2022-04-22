import pytest
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from epic_app.models.epic_answers import (
    Answer,
    MultipleChoiceAnswer,
    SingleChoiceAnswer,
    YesNoAnswer,
    YesNoAnswerType,
)
from epic_app.models.epic_questions import (
    EvolutionChoiceType,
    EvolutionQuestion,
    LinkagesQuestion,
    NationalFrameworkQuestion,
)
from epic_app.models.epic_user import EpicOrganization, EpicUser
from epic_app.models.models import Program
from epic_app.serializers.answer_serializer import (
    MultipleChoiceAnswerSerializer,
    SingleChoiceAnswerSerializer,
    YesNoAnswerSerializer,
)
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
        username="TheOneWhoAsks",
        organization=EpicOrganization.objects.create(name="TestCorp"),
    )
    YesNoAnswer.objects.create(
        user=theonewhoasks,
        question=NationalFrameworkQuestion.objects.all().first(),
        short_answer=YesNoAnswerType.YES,
        justify_answer="Velit ex cupidatat do magna ipsum.",
    )
    SingleChoiceAnswer.objects.create(
        user=theonewhoasks,
        question=EvolutionQuestion.objects.all().first(),
        selected_choice=EvolutionChoiceType.ENGAGED,
        justify_answer="Ipsum anim fugiat sit nostrud enim.",
    )
    mca = MultipleChoiceAnswer.objects.create(
        user=theonewhoasks,
        question=LinkagesQuestion.objects.all().first(),
    )
    mca.selected_programs.add(Program.objects.all()[4], Program.objects.all()[2])


def get_serializer():
    factory = APIRequestFactory()
    request = factory.get("/")

    return {
        "request": Request(request),
    }


serializer_context = get_serializer()


@pytest.mark.django_db
class TestAnswerSerializer:
    @pytest.mark.parametrize(
        "serializer, answer_type, expected_data",
        [
            pytest.param(
                YesNoAnswerSerializer,
                YesNoAnswer,
                {
                    "url": "http://testserver/api/yesnoanswer/1/",
                    "id": 1,
                    "user": 4,
                    "question": 1,
                    "short_answer": "Y",
                    "justify_answer": "Velit ex cupidatat do magna ipsum.",
                },
            ),
            pytest.param(
                SingleChoiceAnswerSerializer,
                SingleChoiceAnswer,
                {
                    "id": 2,
                    "justify_answer": "Ipsum anim fugiat sit nostrud enim.",
                    "question": 3,
                    "selected_choice": "Engaged",
                    "url": "http://testserver/api/singleanswer/2/",
                    "user": 4,
                },
            ),
            pytest.param(
                MultipleChoiceAnswerSerializer,
                MultipleChoiceAnswer,
                {
                    "id": 3,
                    "question": 5,
                    "selected_programs": [3, 5],
                    "url": "http://testserver/api/multianswer/3/",
                    "user": 4,
                },
            ),
        ],
    )
    def test_given_valid_instances_serializer_returns_type_expected_data(
        self, serializer, answer_type: Answer, expected_data: dict
    ):
        serialized_data = list(
            serializer(
                answer_type.objects.all(),
                many=True,
                context=serializer_context,
            ).data
        )

        assert len(serialized_data) == 1
        assert serialized_data[0] == expected_data

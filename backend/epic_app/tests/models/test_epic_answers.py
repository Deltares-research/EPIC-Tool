import pytest

from epic_app.models.epic_answers import (
    Answer,
    MultipleChoiceAnswer,
    SingleChoiceAnswer,
    YesNoAnswer,
)
from epic_app.models.epic_questions import (
    EvolutionQuestion,
    LinkagesQuestion,
    NationalFrameworkQuestion,
    Question,
)
from epic_app.models.epic_user import EpicUser
from epic_app.models.models import Program
from epic_app.tests.epic_db_fixture import epic_test_db


@pytest.fixture(autouse=True)
def EpicAnswersFixture(epic_test_db: pytest.fixture):
    """
    Dummy fixture just to load a default db from dummy_db.

    Args:
        epic_test_db (pytest.fixture): Fixture to load for the whole file tests.
    """
    pass


@pytest.mark.django_db
class TestEpicAnswer:
    @pytest.mark.parametrize(
        "q_type",
        [
            pytest.param(NationalFrameworkQuestion, id="NationalFrameworkQuestion"),
            pytest.param(EvolutionQuestion, id="EvolutionQuestion"),
            pytest.param(LinkagesQuestion, id="LinkagesQuestion"),
        ],
    )
    def test_get_answer_returns_new_instance_when_doesnot_exist(self, q_type: Question):
        q_instance: Question = q_type.objects.all().last()
        u_question: EpicUser = EpicUser.objects.all().last()
        assert not Answer.objects.filter(user=u_question, question=q_instance).exists()

        # Try to get the answer for the first time.
        nf_answer: Answer = q_instance.get_answer(u_question)
        assert Answer.objects.filter(user=u_question, question=q_instance).exists()

        # Try to get it again
        nf_answer_two: Answer = q_instance.get_answer(u_question)
        assert nf_answer == nf_answer_two

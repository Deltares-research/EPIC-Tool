import pytest
from django.db import IntegrityError

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
    KeyAgencyActionsQuestion,
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


# @pytest.mark.django_db
# class TestEpicAnswer:
#     @pytest.mark.parametrize(
#         "q_type",
#         [
#             pytest.param(NationalFrameworkQuestion, id="NationalFrameworkQuestion"),
#             pytest.param(EvolutionQuestion, id="EvolutionQuestion"),
#             pytest.param(LinkagesQuestion, id="LinkagesQuestion"),
#         ],
#     )
#     def test_get_answer_returns_new_instance_when_doesnot_exist(self, q_type: Question):
#         q_instance: Question = q_type.objects.all().last()
#         u_question: EpicUser = EpicUser.objects.all().last()
#         assert not Answer.objects.filter(user=u_question, question=q_instance).exists()

#         # Try to get the answer for the first time.
#         nf_answer: Answer = q_instance.get_answer(u_question)
#         assert Answer.objects.filter(user=u_question, question=q_instance).exists()

#         # Try to get it again
#         nf_answer_two: Answer = q_instance.get_answer(u_question)
#         assert nf_answer == nf_answer_two
@pytest.mark.django_db
class TestYesNoAnswer:
    @pytest.mark.parametrize(
        "unsupported_type",
        [pytest.param(EvolutionQuestion), pytest.param(LinkagesQuestion)],
    )
    def test_SAVE_unsupported_type_raises_integrityerror(
        self, unsupported_type: Question
    ):
        # Define test data
        question_instance = unsupported_type.objects.all().first()
        assert isinstance(question_instance, Question)

        # Run test
        with pytest.raises(IntegrityError) as ie_exc:
            YesNoAnswer.objects.create(
                short_answer=YesNoAnswerType.NO,
                justify_answer="Magna laboris ex Lorem dolor mollit eiusmod occaecat deserunt reprehenderit labore velit ad excepteur.",
                question=question_instance,
                user=EpicUser.objects.all().first(),
            )

        # Verify final expectations.
        assert (
            str(ie_exc.value)
            == f"Answer type {unsupported_type.__name__} not allowed. Supported types: NationalFrameworkQuestion, KeyAgencyActionsQuestion"
        )

    @pytest.mark.parametrize(
        "supported_type",
        [
            pytest.param(NationalFrameworkQuestion),
            pytest.param(KeyAgencyActionsQuestion),
        ],
    )
    def test_SAVE_supported_type_succeeds(self, supported_type: Question):
        # Define test data
        question_instance = supported_type.objects.all().first()
        assert isinstance(question_instance, Question)

        # Run test
        obj_created = YesNoAnswer.objects.create(
            short_answer=YesNoAnswerType.NO,
            justify_answer="Magna laboris ex Lorem dolor mollit eiusmod occaecat deserunt reprehenderit labore velit ad excepteur.",
            question=question_instance,
            user=EpicUser.objects.all().first(),
        )

        # Verify final expectations.
        assert isinstance(obj_created, YesNoAnswer)


@pytest.mark.django_db
class TestSingleChoiceAnswer:
    @pytest.mark.parametrize(
        "unsupported_type",
        [
            pytest.param(LinkagesQuestion),
            pytest.param(NationalFrameworkQuestion),
            pytest.param(KeyAgencyActionsQuestion),
        ],
    )
    def test_SAVE_unsupported_type_raises_integrityerror(
        self, unsupported_type: Question
    ):
        # Define test data
        question_instance = unsupported_type.objects.all().first()
        assert isinstance(question_instance, Question)

        # Run test
        with pytest.raises(IntegrityError) as ie_exc:
            SingleChoiceAnswer.objects.create(
                selected_choice=EvolutionChoiceType.NASCENT,
                justify_answer="Magna laboris ex Lorem dolor mollit eiusmod occaecat deserunt reprehenderit labore velit ad excepteur.",
                question=question_instance,
                user=EpicUser.objects.all().first(),
            )

        # Verify final expectations.
        assert (
            str(ie_exc.value)
            == f"Answer type {unsupported_type.__name__} not allowed. Supported types: EvolutionQuestion"
        )

    def test_SAVE_supported_type_succeeds(self):
        # Define test data
        question_instance = EvolutionQuestion.objects.all().first()
        assert isinstance(question_instance, Question)

        # Run test
        obj_created = SingleChoiceAnswer.objects.create(
            selected_choice=EvolutionChoiceType.NASCENT,
            justify_answer="Magna laboris ex Lorem dolor mollit eiusmod occaecat deserunt reprehenderit labore velit ad excepteur.",
            question=question_instance,
            user=EpicUser.objects.all().first(),
        )

        # Verify final expectations.
        assert isinstance(obj_created, SingleChoiceAnswer)


@pytest.mark.django_db
class TestMultipleChoiceAnswer:
    @pytest.mark.parametrize(
        "unsupported_type",
        [
            pytest.param(EvolutionQuestion),
            pytest.param(NationalFrameworkQuestion),
            pytest.param(KeyAgencyActionsQuestion),
        ],
    )
    def test_SAVE_unsupported_type_raises_integrityerror(
        self, unsupported_type: Question
    ):
        # Define test data
        question_instance = unsupported_type.objects.all().first()
        assert isinstance(question_instance, Question)

        # Run test
        with pytest.raises(IntegrityError) as ie_exc:
            MultipleChoiceAnswer.objects.create(
                question=question_instance,
                user=EpicUser.objects.all().first(),
            )

        # Verify final expectations.
        assert (
            str(ie_exc.value)
            == f"Answer type {unsupported_type.__name__} not allowed. Supported types: LinkagesQuestion"
        )

    def test_SAVE_supported_type_succeeds(self):
        # Define test data
        question_instance = LinkagesQuestion.objects.all().first()
        assert isinstance(question_instance, Question)

        # Run test
        obj_created = MultipleChoiceAnswer.objects.create(
            question=question_instance,
            user=EpicUser.objects.all().first(),
        )

        # Verify final expectations.
        assert isinstance(obj_created, MultipleChoiceAnswer)

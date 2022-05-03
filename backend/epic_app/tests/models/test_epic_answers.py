import itertools
from typing import List

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
from epic_app.tests.epic_db_fixture import epic_test_db


@pytest.fixture(autouse=True)
def EpicAnswersFixture(epic_test_db: pytest.fixture):
    """
    Dummy fixture just to load a default db from dummy_db.

    Args:
        epic_test_db (pytest.fixture): Fixture to load for the whole file tests.
    """
    pass


def get_subtypes(model):
    subtypes = []
    for m in model.__subclasses__():
        if m.__subclasses__():
            subtypes.append(m.__subclasses__())
        else:
            subtypes.append([m])
    return list(itertools.chain(*subtypes))


@pytest.mark.django_db
class TestEpicAnswers:

    answer_ctor: dict = {
        MultipleChoiceAnswer: dict(),
        SingleChoiceAnswer: dict(
            selected_choice=EvolutionChoiceType.NASCENT,
            justify_answer="Magna laboris ex Lorem dolor mollit eiusmod occaecat deserunt reprehenderit labore velit ad excepteur.",
        ),
        YesNoAnswer: dict(
            short_answer=YesNoAnswerType.NO,
            justify_answer="Magna laboris ex Lorem dolor mollit eiusmod occaecat deserunt reprehenderit labore velit ad excepteur.",
        ),
    }

    def test_answer_ctor(self):
        # Define input data.
        epic_question = Question.objects.all().first()
        epic_user = EpicUser.objects.all().first()

        # Instantiate answer.
        base_answer = Answer(question=epic_question, user=epic_user)

        # Verify final expectations.
        assert str(epic_question) in str(base_answer)
        assert str(epic_user) in str(base_answer)
        assert not base_answer._get_supported_questions()
        assert not base_answer._check_question_integrity()
        with pytest.raises(IntegrityError) as err_info:
            base_answer.save()
        assert (
            str(err_info.value)
            == "Question type `Question` not allowed. Supported types: []."
        )

    @pytest.mark.parametrize(
        "question_subtype",
        get_subtypes(Question),
    )
    @pytest.mark.parametrize("answer_subtype", get_subtypes(Answer))
    def test_SAVE_answer(self, question_subtype: Question, answer_subtype: Answer):
        # Define test data
        if not answer_subtype in self.answer_ctor.keys():
            # Check the key exists (doing a .get(key, None) would always check to false for linkages)
            pytest.fail(f"No test input defined for answer type: {answer_subtype}")

        answer_args = self.answer_ctor[answer_subtype]
        answer_args["question"] = question_subtype.objects.all().first()
        answer_args["user"] = EpicUser.objects.all().first()
        assert isinstance(answer_args["question"], Question)

        # Run test and verify expectations.
        answer_instance: Answer = answer_subtype(**answer_args)
        assert not answer_instance in list(answer_subtype.objects.all())

        if question_subtype in answer_instance._get_supported_questions():
            # Run test
            answer_instance.save()
            # Verify final expectations.
            assert answer_instance in list(answer_subtype.objects.all())
        else:
            # Run test
            with pytest.raises(IntegrityError) as ie_exc:
                answer_instance.save()

            # Verify final expectations.
            supported_answers: str = ", ".join(
                [
                    f"`{sq.__name__}`"
                    for sq in answer_instance._get_supported_questions()
                ]
            )
            assert (
                str(ie_exc.value)
                == f"Question type `{question_subtype.__name__}` not allowed. Supported types: [{supported_answers}]."
            )

    @pytest.mark.parametrize(
        "question_subtype, answer_subtype",
        [
            pytest.param(NationalFrameworkQuestion, YesNoAnswer),
            pytest.param(KeyAgencyActionsQuestion, YesNoAnswer),
            pytest.param(EvolutionQuestion, SingleChoiceAnswer),
            pytest.param(LinkagesQuestion, MultipleChoiceAnswer)
        ]
    )
    def test_SAVE_twice_answer_will_raise_integrity_error(self, question_subtype: Question, answer_subtype: Answer):
        with pytest.raises(IntegrityError):
            # Create it once, there should be no problem
            self.test_SAVE_answer(question_subtype, answer_subtype)
            # Create it twice, it should trigger an update instead of create.
            self.test_SAVE_answer(question_subtype, answer_subtype)
        
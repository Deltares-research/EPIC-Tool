from multiprocessing.sharedctypes import Value

import pytest
from rest_framework import serializers

from epic_app.models.epic_answers import YesNoAnswer
from epic_app.models.epic_questions import NationalFrameworkQuestion, Question
from epic_app.models.epic_user import EpicUser
from epic_app.models.models import Program
from epic_app.serializers.progress_serializer import (
    ProgressSerializer,
    _QuestionAnswerSerializer,
)
from epic_app.tests.epic_db_fixture import epic_test_db


@pytest.mark.django_db
class TestQuestionAnswerSerializer:
    def test_ctor(self):
        serializer = _QuestionAnswerSerializer()
        assert isinstance(serializer, serializers.BaseSerializer)

    def test_to_representation_valid_instance(self, epic_test_db):
        q_instance = NationalFrameworkQuestion.objects.first()
        a_user = EpicUser.objects.first()
        a_instance, _ = YesNoAnswer.objects.get_or_create(
            question=q_instance, user=a_user
        )
        serializer = _QuestionAnswerSerializer()
        json_dict = serializer.to_representation((q_instance, a_instance))
        assert json_dict == {q_instance.id: a_instance.id}

    def test_to_representation_invalid_question(self, epic_test_db):
        q_instance = NationalFrameworkQuestion.objects.first()
        a_user = EpicUser.objects.first()
        a_instance, _ = YesNoAnswer.objects.get_or_create(
            question=q_instance, user=a_user
        )
        serializer = _QuestionAnswerSerializer()
        with pytest.raises(ValueError) as err_info:
            serializer.to_representation((None, a_instance))
        assert str(err_info.value) == "No valid question provided."

    def test_to_representation_no_answer(self, epic_test_db):
        q_instance = NationalFrameworkQuestion.objects.first()
        serializer = _QuestionAnswerSerializer()
        assert serializer.to_representation((q_instance, None)) == {q_instance.id: None}


@pytest.mark.django_db
class TestProgressSerializer:

    def test_ctor(self):
        assert isinstance(ProgressSerializer(), serializers.BaseSerializer)
    
    class _FakeRequest:
        user: EpicUser

    def test_to_representation_invalid_instance_raises(self, epic_test_db):
        serializer = ProgressSerializer()
        with pytest.raises(ValueError) as err_info:
            serializer.to_representation(None)
        assert str(err_info.value) == f"Expected instance type {type(Program)}, got {type(None)}"

    def test_to_representation_no_request_in_context_raises(self, epic_test_db):
        # Initialize serializer
        progress_serializer = ProgressSerializer()
        with pytest.raises(ValueError) as err_info:
            progress_serializer.to_representation(Program.objects.get(name="a"))
        
        assert str(err_info.value) == "No user found in context-request."

    def test_to_representation_no_user_in_context_raises(self, epic_test_db):
        # Initialize serializer
        progress_serializer = ProgressSerializer(context={"request": self._FakeRequest()})
        with pytest.raises(ValueError) as err_info:
            progress_serializer.to_representation(Program.objects.get(name="a"))
        
        assert str(err_info.value) == "No user found in context-request."


    def test_to_representation_program(self, epic_test_db):
        # This is better tested in the end-to-end test:
        # test_rest_framework_url.py::test_RETRIEVE_progress_epic_user
        # Therefore we will keep this one simple.
        # Define test data.
        program = Program.objects.get(name="a")
        fr = self._FakeRequest()
        fr.user = EpicUser.objects.first()        
        
        # Initialize serializer
        progress_serializer = ProgressSerializer(context={"request": fr})
        serialized_dict = progress_serializer.to_representation(program)

        # Verify final expectations
        assert list(serialized_dict.keys()) == ["progress", "questions_answers"]
        assert serialized_dict["progress"] == 0.0
        qa_dict = serialized_dict["questions_answers"]
        assert isinstance(qa_dict, dict)
        assert list(qa_dict.keys()) == [q.id for q in program.questions.all()]
        
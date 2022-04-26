from pathlib import Path
from typing import Tuple

import pytest

from epic_app.importers.xlsx.base_importer import BaseEpicImporter, ProtocolEpicImporter
from epic_app.importers.xlsx.question_importer import (
    EvolutionQuestionImporter,
    KeyAgencyActionsQuestionImporter,
    NationalFrameworkQuestionImporter,
    _YesNoJustifyQuestionImporter,
)
from epic_app.models.epic_questions import (
    EvolutionQuestion,
    KeyAgencyActionsQuestion,
    NationalFrameworkQuestion,
    Question,
)
from epic_app.tests import test_data_dir
from epic_app.tests.importers.xlsx.epic_domain_import_fixture import (
    default_epic_domain_data,
)


@pytest.mark.django_db
class TestYesNoJustifyQuestionImporter:
    question_type_dict: dict = {
        KeyAgencyActionsQuestionImporter: dict(
            test_file=test_data_dir / "xlsx" / "keyagencyactionsquestions.xlsx",
            question_type=KeyAgencyActionsQuestion,
            expected_entries=0,
        ),
        NationalFrameworkQuestionImporter: dict(
            test_file=test_data_dir / "xlsx" / "nationalframeworkquestions.xlsx",
            question_type=NationalFrameworkQuestion,
            expected_entries=43,
            first_entry_title="Is there a national strategic water resources management plan in place?",
        ),
    }

    @pytest.mark.parametrize("question_type", question_type_dict.keys())
    def test_yesnoquestion_type_importer(
        self, question_type: _YesNoJustifyQuestionImporter
    ):
        domain_importer = question_type()
        assert isinstance(domain_importer, _YesNoJustifyQuestionImporter)
        assert isinstance(domain_importer, BaseEpicImporter)
        assert isinstance(domain_importer, ProtocolEpicImporter)

    @pytest.mark.parametrize(
        "question_type_fixture",
        question_type_dict.items(),
        ids=question_type_dict.keys(),
    )
    def test_import_file_from_filepath(
        self,
        question_type_fixture: Tuple[_YesNoJustifyQuestionImporter, dict],
        default_epic_domain_data,
    ):
        importer_type, dict_values = question_type_fixture
        question_type: Question = dict_values["question_type"]
        test_file: Path = dict_values["test_file"]
        assert test_file.is_file(), f"Test file not found at {test_file}"

        assert len(question_type.objects.all()) == 0

        importer_type().import_file(test_file)
        assert len(question_type.objects.all()) == dict_values["expected_entries"]
        assert question_type.objects.first().title == dict_values["first_entry_title"]


@pytest.mark.django_db
class TestEvolutionQuestionImporter:
    def test_evolutionquestion_importer(self):
        domain_importer = EvolutionQuestionImporter()
        assert isinstance(domain_importer, BaseEpicImporter)
        assert isinstance(domain_importer, ProtocolEpicImporter)

    def test_import_file_from_filepath(self, default_epic_domain_data):
        test_file = test_data_dir / "xlsx" / "evolutionquestions.xlsx"
        assert test_file.is_file()

        assert len(EvolutionQuestion.objects.all()) == 0

        EvolutionQuestionImporter().import_file(test_file)

        assert len(EvolutionQuestion.objects.all()) == 51

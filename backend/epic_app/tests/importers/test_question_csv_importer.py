import pytest

from epic_app.importers.csv_base_importer import BaseEpicImporter, ProtocolEpicImporter
from epic_app.importers.question_csv_importer import (
    EvolutionQuestionImporter,
    KeyAgencyActionsQuestionImporter,
    NationalFrameworkQuestionImporter,
)
from epic_app.models.epic_questions import (
    EvolutionQuestion,
    KeyAgencyActionsQuestion,
    NationalFrameworkQuestion,
)
from epic_app.tests import test_data_dir
from epic_app.tests.importers.epic_domain_import_fixture import default_epic_domain_data


@pytest.mark.django_db
class TestNationalFrameworkQuestionImporter:
    def test_nationalframeworkquestion_importer(self):
        domain_importer = NationalFrameworkQuestionImporter()
        assert isinstance(domain_importer, BaseEpicImporter)
        assert isinstance(domain_importer, ProtocolEpicImporter)

    def test_import_csv_from_filepath(self, default_epic_domain_data):
        test_file = test_data_dir / "nationalframeworkquestions.csv"
        assert test_file.is_file()

        assert len(NationalFrameworkQuestion.objects.all()) == 0

        NationalFrameworkQuestionImporter().import_csv(test_file)

        assert len(NationalFrameworkQuestion.objects.all()) == 4
        assert (
            NationalFrameworkQuestion.objects.last().title
            == "You will be adding more, won't you?"
        )


@pytest.mark.django_db
class TestKeyAgencyActionsQuestionImporter:
    def test_keyagencyactionsquestion_importer(self):
        domain_importer = KeyAgencyActionsQuestionImporter()
        assert isinstance(domain_importer, BaseEpicImporter)
        assert isinstance(domain_importer, ProtocolEpicImporter)

    def test_import_csv_from_filepath(self, default_epic_domain_data):
        test_file = test_data_dir / "keyagencyactionsquestions.csv"
        assert test_file.is_file()

        assert len(KeyAgencyActionsQuestion.objects.all()) == 0

        KeyAgencyActionsQuestionImporter().import_csv(test_file)

        assert len(KeyAgencyActionsQuestion.objects.all()) == 4


@pytest.mark.django_db
class TestEvolutionQuestionImporter:
    def test_evolutionquestion_importer(self):
        domain_importer = EvolutionQuestionImporter()
        assert isinstance(domain_importer, BaseEpicImporter)
        assert isinstance(domain_importer, ProtocolEpicImporter)

    def test_import_csv_from_filepath(self, default_epic_domain_data):
        test_file = test_data_dir / "evolutionquestions.csv"
        assert test_file.is_file()

        assert len(EvolutionQuestion.objects.all()) == 0

        EvolutionQuestionImporter().import_csv(test_file)

        assert len(EvolutionQuestion.objects.all()) == 5

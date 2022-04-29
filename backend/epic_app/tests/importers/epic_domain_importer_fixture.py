from typing import Type

import pytest

from epic_app.importers.xlsx import EpicDomainImporter
from epic_app.importers.xlsx.agency_importer import EpicAgencyImporter
from epic_app.importers.xlsx.base_importer import BaseEpicImporter
from epic_app.importers.xlsx.question_importer import (
    EvolutionQuestionImporter,
    KeyAgencyActionsQuestionImporter,
    NationalFrameworkQuestionImporter,
)
from epic_app.models.epic_questions import LinkagesQuestion
from epic_app.tests import test_data_dir


@pytest.fixture(autouse=False)
def default_epic_domain_data():
    """
    Fixture to load the predefined database so we can test importing agencies correctly.
    """
    # Define test data
    test_file = test_data_dir / "xlsx" / "initial_epic_data.xlsx"
    assert test_file.is_file()
    EpicDomainImporter().import_file(test_file)


@pytest.fixture(autouse=False)
def full_epic_domain_data():
    def _import(filename: str, importer: Type[BaseEpicImporter]):
        test_file = test_data_dir / "xlsx" / filename
        assert test_file.is_file()
        importer().import_file(test_file)

    _import("initial_epic_data.xlsx", EpicDomainImporter)
    _import("agency_data.xlsx", EpicAgencyImporter)
    _import("nationalframeworkquestions.xlsx", NationalFrameworkQuestionImporter)
    _import("keyagencyactionsquestions.xlsx", KeyAgencyActionsQuestionImporter)
    _import("evolutionquestions.xlsx", EvolutionQuestionImporter)
    LinkagesQuestion.generate_linkages()

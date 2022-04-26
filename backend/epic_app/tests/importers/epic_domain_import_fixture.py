import pytest

from epic_app.importers.domain_csv_importer import EpicDomainImporter
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

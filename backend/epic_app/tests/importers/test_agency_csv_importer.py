import pytest

from epic_app.importers import BaseEpicImporter, EpicAgencyImporter
from epic_app.importers.xlsx_base_importer import ProtocolEpicImporter
from epic_app.models.models import Agency
from epic_app.tests import test_data_dir
from epic_app.tests.importers.epic_domain_import_fixture import default_epic_domain_data


class TestEpicAgencyImporter:
    @pytest.mark.django_db
    def test_epic_agency_importer(self):
        agency_importer = EpicAgencyImporter()
        assert isinstance(agency_importer, BaseEpicImporter)
        assert isinstance(agency_importer, ProtocolEpicImporter)

    @pytest.mark.django_db
    def test_import_file_from_filepath(self, default_epic_domain_data):
        # Define test data
        test_file = test_data_dir / "xlsx" / "agency_data.xlsx"
        assert test_file.is_file()

        # Verify initial expectations
        dummy_agency = Agency(name="dummyAgency")
        dummy_agency.save()
        assert len(Agency.objects.all()) == 1

        # Run test
        EpicAgencyImporter().import_file(test_file)

        # Verify final expectations
        assert len(Agency.objects.all()) == 6

        # Verify the initial data has been removed.
        assert dummy_agency not in Agency.objects.all()

from io import BytesIO
from pathlib import Path

import pytest
from django.core.files.uploadedfile import InMemoryUploadedFile

from epic_app.importers import EpicAgencyImporter, EpicDomainImporter, EpicImporter
from epic_app.models.models import Agency, Area, Group, Program

test_data_dir: Path = Path(__file__).parent.parent / "test_data"


class TestEpicDomainImporter:
    def test_epic_domain_importer(self):
        importer = EpicDomainImporter()
        assert isinstance(importer, EpicImporter)

    @pytest.mark.django_db
    def test_import_csv_from_filepath(self):
        # Define test data
        test_file = test_data_dir / "initial_epic_data.csv"
        assert test_file.is_file()

        # Verify initial expectations
        dummy_area = Area(name="dummyArea")
        dummy_area.save()
        dummy_group = Group(name="dummyGroup", area=dummy_area)
        dummy_group.save()
        dummy_program = Program(name="dummyProgram", group=dummy_group)
        dummy_program.save()
        assert len(Area.objects.all()) == 1
        assert len(Group.objects.all()) == 1
        assert len(Program.objects.all()) == 1

        # Run test
        EpicDomainImporter().import_csv(test_file)

        # Verify final expectations
        assert len(Area.objects.all()) == 5
        assert len(Group.objects.all()) == 11
        assert len(Program.objects.all()) == 43
        assert any(
            [p.description != "" for p in Program.objects.all()]
        ), "No descriptions were imported."
        # Verify the initial data has been removed.
        assert dummy_area not in Area.objects.all()
        assert dummy_group not in Group.objects.all()
        assert dummy_program not in Program.objects.all()

    @pytest.mark.django_db
    def test_import_csv_from_inmemoryuploaddedfile(self):
        # Define request.
        test_file = test_data_dir / "initial_epic_data.csv"
        assert test_file.is_file()
        with test_file.open("rb") as csv_file:
            file_io = BytesIO(csv_file.read())
            file_io.name = test_file.name
            file_io.seek(0)
        csv_inmemoryfile = InMemoryUploadedFile(
            file_io,
            None,
            file_io.name,
            "application/vnd.ms-excel",
            len(file_io.getvalue()),
            None,
        )

        # Verify initial expectations
        dummy_area = Area(name="dummyArea")
        dummy_area.save()
        dummy_group = Group(name="dummyGroup", area=dummy_area)
        dummy_group.save()
        dummy_program = Program(name="dummyProgram", group=dummy_group)
        dummy_program.save()
        assert len(Area.objects.all()) == 1
        assert len(Group.objects.all()) == 1
        assert len(Program.objects.all()) == 1

        # Run test
        EpicDomainImporter().import_csv(csv_inmemoryfile)

        # Verify final expectations
        assert len(Area.objects.all()) == 5
        assert len(Group.objects.all()) == 11
        assert len(Program.objects.all()) == 43
        assert any(
            [p.description != "" for p in Program.objects.all()]
        ), "No descriptions were imported."

        # Verify the initial data has been removed.
        assert dummy_area not in Area.objects.all()
        assert dummy_group not in Group.objects.all()
        assert dummy_program not in Program.objects.all()


class TestEpicAgencyImporter:
    @pytest.fixture(autouse=True)
    @pytest.mark.django_db
    def default_epic_domain_data(self):
        """
        Fixture to load the predefined database so we can test importing agencies correctly.
        """
        # Define test data
        test_file = test_data_dir / "initial_epic_data.csv"
        assert test_file.is_file()
        EpicDomainImporter().import_csv(test_file)

    @pytest.mark.django_db
    def test_epic_agency_importer(self):
        agency_importer = EpicAgencyImporter()
        assert isinstance(agency_importer, EpicImporter)

    @pytest.mark.django_db
    def test_import_csv_from_filepath(self):
        # Define test data
        test_file = test_data_dir / "agency_data.csv"
        assert test_file.is_file()

        # Verify initial expectations
        dummy_agency = Agency(name="dummyAgency")
        dummy_agency.save()
        assert len(Agency.objects.all()) == 1

        # Run test
        EpicAgencyImporter().import_csv(test_file)

        # Verify final expectations
        assert len(Agency.objects.all()) == 6

        # Verify the initial data has been removed.
        assert dummy_agency not in Agency.objects.all()

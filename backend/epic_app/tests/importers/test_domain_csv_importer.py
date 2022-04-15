from io import BytesIO

import pytest
from django.core.files.uploadedfile import InMemoryUploadedFile

from epic_app.importers import BaseEpicImporter, EpicDomainImporter
from epic_app.importers.csv_base_importer import ProtocoEpicImporter
from epic_app.models.models import Area, Group, Program
from epic_app.tests import test_data_dir


@pytest.mark.django_db
class TestEpicDomainImporter:
    def test_epic_domain_importer(self):
        domain_importer = EpicDomainImporter()
        assert isinstance(domain_importer, BaseEpicImporter)
        assert isinstance(domain_importer, ProtocoEpicImporter)

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
        assert len(Program.objects.all()) == 42
        assert any(
            [p.description != "" for p in Program.objects.all()]
        ), "No descriptions were imported."
        # Verify the initial data has been removed.
        assert dummy_area not in Area.objects.all()
        assert dummy_group not in Group.objects.all()
        assert dummy_program not in Program.objects.all()

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
        assert len(Program.objects.all()) == 42
        assert any(
            [p.description != "" for p in Program.objects.all()]
        ), "No descriptions were imported."

        # Verify the initial data has been removed.
        assert dummy_area not in Area.objects.all()
        assert dummy_group not in Group.objects.all()
        assert dummy_program not in Program.objects.all()

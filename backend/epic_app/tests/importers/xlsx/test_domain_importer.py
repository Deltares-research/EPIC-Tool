from io import BytesIO

import pytest
from django.core.files.uploadedfile import InMemoryUploadedFile

from epic_app.importers.xlsx import BaseEpicImporter, EpicDomainImporter
from epic_app.importers.xlsx.base_importer import ProtocolEpicImporter
from epic_app.models.models import Area, Group, Program
from epic_app.tests import test_data_dir


@pytest.mark.django_db
class TestEpicDomainImporter:
    domain_xlsx_file = test_data_dir / "xlsx" / "initial_epic_data.xlsx"

    def test_epic_domain_importer(self):
        domain_importer = EpicDomainImporter()
        assert isinstance(domain_importer, BaseEpicImporter)
        assert isinstance(domain_importer, ProtocolEpicImporter)

    def test_import_file_from_filepath(self):
        # Define test data
        assert self.domain_xlsx_file.is_file()

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
        EpicDomainImporter().import_file(self.domain_xlsx_file)

        # Verify final expectations
        self._verify_default_import_final_expectations(
            dict(area=dummy_area, group=dummy_group, program=dummy_program)
        )

    def test_import_file_from_inmemoryuploaddedfile(self):
        # Define request.
        assert self.domain_xlsx_file.is_file()
        with self.domain_xlsx_file.open("rb") as csv_file:
            file_io = BytesIO(csv_file.read())
            file_io.name = self.domain_xlsx_file.name
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
        EpicDomainImporter().import_file(csv_inmemoryfile)

        # Verify final expectations
        self._verify_default_import_final_expectations(
            dict(area=dummy_area, group=dummy_group, program=dummy_program)
        )

    def _verify_default_import_final_expectations(self, dummy_set: dict):
        # Verify final expectations
        assert len(Area.objects.all()) == 5
        assert len(Group.objects.all()) == 11
        assert len(Program.objects.all()) == 43
        assert any(
            [p.description != "" for p in Program.objects.all()]
        ), "No descriptions were imported."
        # Verify the initial data has been removed.
        assert dummy_set["area"] not in Area.objects.all()
        assert dummy_set["group"] not in Group.objects.all()
        assert dummy_set["program"] not in Program.objects.all()

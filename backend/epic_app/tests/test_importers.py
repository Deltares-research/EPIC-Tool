from io import BytesIO
from epic_app.importers import EpicDomainImporter
from epic_app.models import Area, Group, Program
from django.core.files.uploadedfile import InMemoryUploadedFile
from pathlib import Path
import pytest


class TestEpicDomainImporter:
   
    @pytest.mark.django_db
    def test_import_csv_from_filepath(self):
        # Define test data
        test_file = Path(__file__).parent / "test_data" / "initial_epic_data.csv"
        assert test_file.is_file()

        # Verify initial expectations       
        dummy_area = Area(name="dummyArea")
        dummy_area.save()
        dummy_group = Group(name="dummyGroup", area = dummy_area)
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
        # Verify the initial data has been removed.
        assert dummy_area not in Area.objects.all()
        assert dummy_group not in Group.objects.all()
        assert dummy_program not in Program.objects.all()

    @pytest.mark.django_db
    def test_import_csv_from_inmemoryuploaddedfile(self):
        # Define request.
        test_file = Path(__file__).parent / "test_data" / "initial_epic_data.csv"
        assert test_file.is_file()
        with test_file.open("rb") as csv_file:
            file_io = BytesIO(csv_file.read())
            file_io.name = test_file.name
            file_io.seek(0)
        csv_inmemoryfile = InMemoryUploadedFile(file_io, None, file_io.name,'application/vnd.ms-excel', len(file_io.getvalue()), None)

        # Verify initial expectations       
        dummy_area = Area(name="dummyArea")
        dummy_area.save()
        dummy_group = Group(name="dummyGroup", area = dummy_area)
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
        # Verify the initial data has been removed.
        assert dummy_area not in Area.objects.all()
        assert dummy_group not in Group.objects.all()
        assert dummy_program not in Program.objects.all()
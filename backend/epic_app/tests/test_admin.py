from io import BytesIO
from pathlib import Path
from typing import Optional
from wsgiref.simple_server import WSGIRequestHandler

import pytest
from django.contrib import admin
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import RequestFactory

from epic_app.admin import AgencyAdmin, AreaAdmin, ImportEntityAdmin
from epic_app.models.models import Agency, Area, Group, Program


class TestAreaAdmin:
    @pytest.fixture(autouse=False)
    def area_admin_site(self) -> AreaAdmin:
        reg_area = next(
            (r_model for r_model in admin.site._registry if r_model is Area), None
        )
        return admin.site._registry[reg_area]

    @pytest.fixture(autouse=False)
    def csv_inmemoryfile(self) -> InMemoryUploadedFile:
        test_file = Path(__file__).parent / "test_data" / "initial_epic_data.csv"
        assert test_file.is_file()
        with test_file.open("rb") as csv_file:
            file_io = BytesIO(csv_file.read())
            file_io.name = test_file.name
            file_io.seek(0)
        in_memory_file = InMemoryUploadedFile(
            file_io,
            None,
            file_io.name,
            "application/vnd.ms-excel",
            len(file_io.getvalue()),
            None,
        )
        return in_memory_file

    def test_area_admin_is_initialized(self):
        assert admin.site.is_registered(Area)
        reg_area = next(
            (r_model for r_model in admin.site._registry if r_model is Area), None
        )
        assert reg_area is not None, "No Area was registered as a model."
        area_admin = admin.site._registry[reg_area]
        assert isinstance(area_admin, AreaAdmin)
        assert isinstance(area_admin, ImportEntityAdmin)
        assert area_admin.change_list_template == "import_changelist.html"
        assert any("import-csv/" in str(t_url) for t_url in area_admin.urls)

    def test_get_import_csv_returns_success_code(self, area_admin_site: AreaAdmin):
        rf = RequestFactory()
        request = rf.get("import-csv/")
        r_result = area_admin_site.import_csv(request)
        assert r_result is not None
        assert r_result.status_code == 200

    def _post_import_csv_request(
        self, csv_input_file: Optional[InMemoryUploadedFile]
    ) -> WSGIRequestHandler:
        request_factory = RequestFactory()
        post_request = request_factory.post("import-csv/")
        post_request.FILES["csv_file"] = csv_input_file

        # adding session
        middleware = SessionMiddleware(post_request)
        middleware.process_request(post_request)
        post_request.session.save()

        # adding messages
        messages = FallbackStorage(post_request)
        setattr(post_request, "_messages", messages)
        return post_request

    @pytest.mark.django_db
    def test_post_import_csv_with_valid_data_imports_and_redirects(
        self, csv_inmemoryfile: InMemoryUploadedFile, area_admin_site: AreaAdmin
    ):
        # Define request.
        post_request = self._post_import_csv_request(csv_inmemoryfile)

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
        r_result = area_admin_site.import_csv(post_request)

        # Verify final expectations
        assert r_result is not None
        # Status code is redirected.
        assert r_result.status_code == 302
        assert r_result.url == ".."
        assert len(Area.objects.all()) == 5
        assert len(Group.objects.all()) == 11
        assert len(Program.objects.all()) == 43
        # Verify the initial data has been removed.
        assert dummy_area not in Area.objects.all()
        assert dummy_group not in Group.objects.all()
        assert dummy_program not in Program.objects.all()

    @pytest.mark.django_db
    def test_post_import_csv_with_empty_data_imports_and_redirects(
        self, area_admin_site: AreaAdmin
    ):
        # Define request.
        post_request = self._post_import_csv_request(None)

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
        r_result = area_admin_site.import_csv(post_request)

        # Verify final expectations
        assert r_result is not None
        # Status code is redirected.
        assert r_result.status_code == 302
        assert r_result.url == ".."
        # Status has not changed.
        assert len(Area.objects.all()) == 1
        assert len(Group.objects.all()) == 1
        assert len(Program.objects.all()) == 1
        # Verify the initial data has been not removed.
        assert dummy_area in Area.objects.all()
        assert dummy_group in Group.objects.all()
        assert dummy_program in Program.objects.all()


class TestAgencyAdmin:
    def test_agency_admin_is_initialized(self):
        assert admin.site.is_registered(Agency)
        reg_agency = next(
            (r_model for r_model in admin.site._registry if r_model is Agency), None
        )
        assert reg_agency is not None, "No Agency was registered as a model."
        agency_admin = admin.site._registry[reg_agency]
        assert isinstance(agency_admin, AgencyAdmin)
        assert isinstance(agency_admin, ImportEntityAdmin)
        assert agency_admin.change_list_template == "import_changelist.html"
        assert any("import-csv/" in str(t_url) for t_url in agency_admin.urls)

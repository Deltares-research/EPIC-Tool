from io import BytesIO
from pathlib import Path
from typing import Optional
from epic_app.admin import AreaAdmin
from epic_app.models import Area
from django.contrib import admin
from django.test import RequestFactory
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware

import pytest

def csv_inmemoryfile() -> InMemoryUploadedFile:
    test_file = Path(__file__).parent / "test_data" / "initial_epic_data.csv"
    assert test_file.is_file()
    with test_file.open("rb") as csv_file:
        file_io = BytesIO(csv_file.read())
        file_io.name = test_file.name
        file_io.seek(0)
    in_memory_file = InMemoryUploadedFile(file_io, None, file_io.name,'application/vnd.ms-excel', len(file_io.getvalue()), None)
    return in_memory_file

class TestAreaAdmin():

    @pytest.fixture(autouse=False)
    def area_admin_site(self) -> AreaAdmin:
        reg_area = next(( r_model for r_model in admin.site._registry if r_model is Area), None)
        return admin.site._registry[reg_area]
    def test_area_admin_is_initialized(self):
        assert admin.site.is_registered(Area)
        reg_area = next(( r_model for r_model in admin.site._registry if r_model is Area), None)
        assert reg_area is not None, "No Area was registered as a model."
        area_admin = admin.site._registry[reg_area]
        assert type(area_admin) == AreaAdmin
        assert area_admin.change_list_template == "areas_changelist.html"
        assert any('import-csv/' in str(t_url) for t_url in area_admin.urls)

    def test_get_import_csv_returns_success_code(self, area_admin_site: AreaAdmin):
        rf = RequestFactory()
        request = rf.get('import-csv/')
        r_result = area_admin_site.import_csv(request)
        assert r_result is not None
        assert r_result.status_code == 200
    
    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "input_csv_file",
        [
            pytest.param(csv_inmemoryfile(), id="Valid input"),
            pytest.param("", id="Empty input")]
    )
    def test_post_import_csv_redirects(self, area_admin_site: AreaAdmin, input_csv_file: Optional[InMemoryUploadedFile]):
        # Define request.
        request_factory = RequestFactory()
        post_request = request_factory.post('import-csv/')
        post_request.FILES["csv_file"] = input_csv_file

        # adding session
        middleware = SessionMiddleware(post_request)
        middleware.process_request(post_request)
        post_request.session.save()
        
        # adding messages
        messages = FallbackStorage(post_request)
        setattr(post_request, '_messages', messages)

        # Run test
        r_result = area_admin_site.import_csv(post_request)

        # Verify final expectations
        assert r_result is not None
        # Status code is redirected.
        assert r_result.status_code == 302
        assert r_result.url == '..'

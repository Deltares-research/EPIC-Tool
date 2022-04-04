from epic_app.admin import AreaAdmin
from epic_app.models import Area
from django.contrib import admin


class TestAreaAdmin:
    def test_area_admin_is_initialized(self):
        assert admin.site.is_registered(Area)
        reg_area = next(( r_model for r_model in admin.site._registry if r_model is Area), None)
        assert reg_area is not None, "No Area was registered as a model."
        area_admin = admin.site._registry[reg_area]
        assert type(area_admin) == AreaAdmin
        assert area_admin.change_list_template == "areas_changelist.html"
        assert any('import-csv/' in str(t_url) for t_url in area_admin.urls)
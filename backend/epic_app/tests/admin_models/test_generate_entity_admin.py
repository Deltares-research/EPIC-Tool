import pytest
from django.contrib import admin

from epic_app.admin_models.generate_entity_admin import LnkAdmin
from epic_app.models.epic_questions import LinkagesQuestion
from epic_app.models.models import Agency, Area, Group, Program
from epic_app.tests.importers import default_epic_domain_data, full_epic_domain_data
from epic_app.tests.request_helper import _create_get_request


class TestLinkagesQuestionAdmin:
    def test_linkages_admin_is_initialized(self):
        assert admin.site.is_registered(LinkagesQuestion)
        reg_lquestion = next(
            (
                r_model
                for r_model in admin.site._registry
                if r_model is LinkagesQuestion
            ),
            None,
        )
        assert reg_lquestion is not None, "No Agency was registered as a model."
        agency_admin = admin.site._registry[reg_lquestion]
        assert isinstance(agency_admin, LnkAdmin)
        assert agency_admin.change_list_template == "generate_changelist.html"
        assert any("generate/" in str(t_url) for t_url in agency_admin.urls)

    @pytest.mark.django_db
    def test_get_generate_entities(self, default_epic_domain_data):
        # Define test data
        lq_admin: LnkAdmin = admin.site._registry[
            next(
                r_model
                for r_model in admin.site._registry
                if r_model is LinkagesQuestion
            )
        ]
        get_request = _create_get_request("generate/")

        # Verify initial expectations
        LinkagesQuestion.objects.all().delete()
        assert len(Program.objects.all()) > 0

        # Run test
        r_result = lq_admin.generate_entities(get_request)

        # Verify expectations
        assert r_result is not None
        # Status code is redirected.
        assert r_result.status_code == 302  # Redirection
        assert r_result.url == ".."
        assert len(LinkagesQuestion.objects.all()) > 0

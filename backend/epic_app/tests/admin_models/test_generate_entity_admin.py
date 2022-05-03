import pytest
from django.contrib import admin
from rest_framework.test import APIClient

from epic_app.admin_models.generate_entity_admin import EpicOrganizationAdmin, LnkAdmin
from epic_app.models.epic_questions import LinkagesQuestion
from epic_app.models.epic_user import EpicOrganization, EpicUser
from epic_app.models.models import Program
from epic_app.tests.epic_db_fixture import epic_test_db
from epic_app.tests.request_helper import (
    _create_get_request,
    _create_post_request,
)


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
        assert agency_admin.actions == ["generate_entities"]

    @pytest.fixture(autouse=False)
    @pytest.mark.django_db
    def api_client(self, epic_test_db) -> APIClient:
        api_client = APIClient()
        api_client.login(username="admin", password="admin")
        return api_client

    @pytest.mark.django_db
    def test_POST_generate_entities(self, api_client: APIClient):
        # Define test data
        data = {"action": "generate_entities"}
        req_url = "/admin/epic_app/linkagesquestion/"

        # Verify initial expectations
        assert len(Program.objects.all()) > 0
        previous_lq_ids = [lq.pk for lq in LinkagesQuestion.objects.all()]

        # Run test
        r_result = api_client.post(
            req_url,
            data,
        )

        # Verify expectations
        assert r_result is not None
        # Status code is redirected.
        assert r_result.status_code == 302  # Redirection
        assert r_result.url == req_url
        assert len(LinkagesQuestion.objects.all()) > 0
        assert not any(
            lq.pk in previous_lq_ids for lq in LinkagesQuestion.objects.all()
        )


class TestEpicOrganizationAdmin:
    def test_epic_organization_admin_is_initialized(self):
        assert admin.site.is_registered(EpicOrganization)
        reg_epic_org = next(
            (
                r_model
                for r_model in admin.site._registry
                if r_model is EpicOrganization
            ),
            None,
        )
        assert (
            reg_epic_org is not None
        ), "No Epic Organization was registered as a model."
        epic_org_admin = admin.site._registry[reg_epic_org]
        assert isinstance(epic_org_admin, EpicOrganizationAdmin)
        assert epic_org_admin.change_list_template == "generate_changelist.html"
        assert any("generate/" in str(t_url) for t_url in epic_org_admin.urls)

    @pytest.mark.django_db
    def test_GET_generate_entities(self, epic_test_db):
        # Define test data
        eo_admin: EpicOrganizationAdmin = admin.site._registry[
            next(
                r_model
                for r_model in admin.site._registry
                if r_model is EpicOrganization
            )
        ]
        get_request = _create_get_request("generate/")

        # Run test
        r_result = eo_admin.generate_entities(get_request)

        # Verify expectations
        assert r_result is not None
        # Status code is redirected.
        assert r_result.status_code == 200  # Redirection

    @pytest.mark.django_db
    def test_POST_generate_entities(self, epic_test_db):
        # Define test data
        EpicUser.objects.all().delete()
        generate_n_users = 42
        eo_admin: EpicOrganizationAdmin = admin.site._registry[
            next(
                r_model
                for r_model in admin.site._registry
                if r_model is EpicOrganization
            )
        ]
        eo_pk: str = str(EpicOrganization.objects.first().pk)
        post_request = _create_post_request(
            "generate/", dict(selected_org=eo_pk, n_epic_users=generate_n_users)
        )

        # Run test
        r_result = eo_admin.generate_entities(post_request)

        # Verify expectations
        assert r_result is not None
        # Status code is redirected.
        assert r_result.status_code == 302  # Redirection
        assert r_result.url == ".."
        assert len(EpicUser.objects.all()) == generate_n_users

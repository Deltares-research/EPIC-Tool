from django.urls import include, path
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

from epic_app import apps, views

router = routers.DefaultRouter()
router.register(r"epicuser", views.EpicUserViewSet)
router.register(r"area", views.AreaViewSet)
router.register(r"agency", views.AgencyViewSet)
router.register(r"group", views.GroupViewSet)
router.register(r"program", views.ProgramViewSet)
router.register(r"nationalframeworkquestion", views.NationalFrameworkQuestionViewSet)
router.register(r"evolutionquestion", views.EvolutionQuestionViewSet)
router.register(r"linkagesquestion", views.LinkagesQuestionViewSet)
router.register(r"yesnoanswer", views.YesNoAnswerViewSet)
router.register(r"singleanswer", views.SingleChoiceAnswerViewSet)
router.register(r"multianswer", views.MultipleChoiceAnswerViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", RedirectView.as_view(url="api/", permanent=False), name="index"),
    path(
        f"admin/{apps.EpicAppConfig.name}",
        RedirectView.as_view(url="api/", permanent=False),
        name=f"admin_{apps.EpicAppConfig.name}",
    ),
    path("api/", include(router.urls), name="api"),
    path("api/api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/token-auth/", obtain_auth_token, name="api_token_auth"),
    path(
        "api/docs/",
        get_schema_view(
            title="EPIC OpenAPI",
            description="API disclosure of all available calls.",
            version="0.11.0",
        ),
        name="openapi-schema",
    ),  # Declaring the openapi schema seems to be mandatory in order to produce the following two
    path(
        "api/docs/reference",
        include_docs_urls(title="EPIC API Reference", public=False),
        name="docs-reference",
    ),
    path(
        "api/docs/swagger",
        TemplateView.as_view(
            template_name="swagger-ui.html",
            extra_context={"schema_url": "openapi-schema"},
        ),
        name="docs-swagger",
    ),
]

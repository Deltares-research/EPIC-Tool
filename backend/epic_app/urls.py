from django.views.generic.base import RedirectView
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from epic_app import views

router = routers.DefaultRouter()
router.register(r'epicuser', views.EpicUserViewSet)
router.register(r'area', views.AreaViewSet)
router.register(r'group', views.GroupViewSet)
router.register(r'program', views.ProgramViewSet)
router.register(r'question', views.QuestionViewSet)
router.register(r'answer', views.AnswerViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', RedirectView.as_view(url='api/', permanent=False), name='index'),
    path('api/', include(router.urls)),
    path('api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token-auth/', obtain_auth_token, name='api_token_auth'),
]

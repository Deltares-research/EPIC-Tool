from django.urls import include, path
from rest_framework import routers
from epic_app import views

router = routers.DefaultRouter()
router.register(r'epicuser', views.EpicUserViewSet)
router.register(r'question', views.QuestionViewSet)
router.register(r'answer', views.AnswerViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'games', views.GameViewSet)
router.register(r'teams', views.TeamViewSet)
router.register(r'scoring_types', views.ScoringTypeViewSet)
router.register(r'game_participants', views.GameParticipantViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
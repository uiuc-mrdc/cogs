from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'teams', views.TeamViewSet)
router.register(r'team_contacts', views.TeamContactViewSet)
router.register(r'schools', views.SchoolViewSet)
router.register(r'contenders', views.ContenderViewSet)
router.register(r'matches', views.MatchViewSet)
router.register(r'matche_state_change_events', views.MatchStateChangeEventViewSet)
router.register(r'contender_positions', views.ContenderPositionViewSet)
router.register(r'contender_context_change_event', views.ContenderContextChangeEventViewSet)
router.register(r'scoring_contexts', views.ScoringContextViewSet)
router.register(r'scoring_type_groups', views.ScoringTypeGroupViewSet)
router.register(r'scoring_types', views.ScoringTypeViewSet)
router.register(r'scoring_events', views.ScoringEventViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
	path('available_teams/', views.AvailableTeamsList.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
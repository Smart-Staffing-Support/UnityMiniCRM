from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    CompanyViewSet,
    ContactViewSet,
    DealViewSet,
    TaskViewSet,
    dashboard_stats,
    login_view,
    logout_view,
)

router = SimpleRouter(trailing_slash=False)
router.register("companies", CompanyViewSet)
router.register("contacts", ContactViewSet)
router.register("deals", DealViewSet)
router.register("tasks", TaskViewSet)

urlpatterns = [
    path("auth/login", login_view),
    path("auth/logout", logout_view),
    path("dashboard/stats", dashboard_stats),
    path("", include(router.urls)),
]

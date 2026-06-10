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

router = SimpleRouter()
router.register("companies", CompanyViewSet)
router.register("contacts", ContactViewSet)
router.register("deals", DealViewSet)
router.register("tasks", TaskViewSet)

urlpatterns = [
    path("auth/login", login_view, name="login"),
    path("auth/logout", logout_view, name="logout"),
    path("dashboard/stats", dashboard_stats, name="dashboard_stats"),
    path("", include(router.urls)),
]

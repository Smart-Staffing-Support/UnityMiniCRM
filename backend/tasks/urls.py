from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CompanyViewSet, ContactViewSet, DealViewSet, TaskViewSet,
    login_view, logout_view, dashboard_stats, TimelineViewSet, NotificationViewSet
)

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'deals', DealViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'timeline', TimelineViewSet, basename='timeline')
router.register(r'notifications', NotificationViewSet, basename='notifications')

urlpatterns = [
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('dashboard/stats/', dashboard_stats, name='dashboard_stats'),
    path('', include(router.urls)),
]

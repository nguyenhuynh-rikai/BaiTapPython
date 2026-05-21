from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AmenityViewSet,
    CategoryViewSet,
    DistrictViewSet,
    PropertyImageViewSet,
    PropertyViewSet,
    WardViewSet,
    FavoritePropertyViewSet,
    ViewingAppointmentViewSet,
    ComparisonViewSet,
)
from .auth_views import ChangePasswordAPIView, LoginAPIView, LogoutAPIView, RegisterAPIView, UserProfileAPIView
from .task_views import ImportPropertiesTaskAPIView, TaskDetailAPIView, TaskListAPIView


router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("districts", DistrictViewSet)
router.register("wards", WardViewSet)
router.register("amenities", AmenityViewSet)
router.register("properties", PropertyViewSet, basename="property")
router.register("property-images", PropertyImageViewSet)
router.register("favorites", FavoritePropertyViewSet, basename="favorite")
router.register("appointments", ViewingAppointmentViewSet, basename="appointment")
router.register("compare", ComparisonViewSet, basename="compare")



urlpatterns = [
    path("auth/register/", RegisterAPIView.as_view()),
    path("auth/login/", LoginAPIView.as_view()),
    path("auth/profile/", UserProfileAPIView.as_view()),
    path("auth/change-password/", ChangePasswordAPIView.as_view()),
    path("auth/logout/", LogoutAPIView.as_view()),
    path("tasks/import-properties/", ImportPropertiesTaskAPIView.as_view()),
    path("tasks/", TaskListAPIView.as_view()),
    path("tasks/<str:task_id>/", TaskDetailAPIView.as_view()),
    path("", include(router.urls)),
]

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AmenityViewSet,
    CategoryViewSet,
    DistrictViewSet,
    PropertyImageViewSet,
    PropertyViewSet,
    WardViewSet,
)
from .auth_views import ChangePasswordAPIView, LoginAPIView, LogoutAPIView, RegisterAPIView


router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("districts", DistrictViewSet)
router.register("wards", WardViewSet)
router.register("amenities", AmenityViewSet)
router.register("properties", PropertyViewSet, basename="property")
router.register("property-images", PropertyImageViewSet)


urlpatterns = [
    path("auth/register/", RegisterAPIView.as_view()),
    path("auth/login/", LoginAPIView.as_view()),
    path("auth/change-password/", ChangePasswordAPIView.as_view()),
    path("auth/logout/", LogoutAPIView.as_view()),
    path("", include(router.urls)),
]

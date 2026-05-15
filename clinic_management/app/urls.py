"""
MediFlow — api/urls.py
========================
Đăng ký toàn bộ URL patterns của API.

Bản đồ endpoints đầy đủ:
─────────────────────────────────────────────────────────────
AUTH
  POST   /api/auth/register/
  POST   /api/auth/login/
  POST   /api/auth/token/refresh/
  GET    /api/auth/me/
  PATCH  /api/auth/me/
  POST   /api/auth/change-password/

CLINIC
  GET    /api/clinics/
  POST   /api/clinics/           [admin]
  GET    /api/clinics/{id}/
  PATCH  /api/clinics/{id}/      [admin]
  DELETE /api/clinics/{id}/      [admin]

DOCTOR
  GET    /api/doctors/
  GET    /api/doctors/{id}/
  GET    /api/doctors/{id}/workload/   [doctor xem mình | admin]
  GET    /api/doctors/{id}/schedule/   [doctor | admin]

PATIENT
  GET    /api/patients/me/
  PATCH  /api/patients/me/
  GET    /api/patients/me/appointments/

SLOT
  GET    /api/slots/available/

APPOINTMENT
  POST   /api/appointments/               [patient]
  GET    /api/appointments/{id}/
  DELETE /api/appointments/{id}/
  PATCH  /api/appointments/{id}/confirm/  [doctor | admin]
  GET    /api/appointments/{id}/medical-record/
  POST   /api/appointments/{id}/medical-record/ [doctor]

DRUG
  GET    /api/drugs/
  GET    /api/drugs/{id}/

PAYMENT
  GET    /api/payments/{id}/
  PATCH  /api/payments/{id}/             [admin]

DOCS (Swagger / Redoc)
  GET    /api/schema/
  GET    /api/docs/        (Swagger UI)
  GET    /api/redoc/
─────────────────────────────────────────────────────────────
"""

from django.urls import include, path
# from drf_spectacular.views import (
#     SpectacularAPIView,
#     SpectacularRedocView,
#     SpectacularSwaggerView,
# )
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from app.views import (
    AppointmentViewSet,
    AvailableSlotsView,
    ChangePasswordView,
    ClinicViewSet,
    DoctorViewSet,
    DrugViewSet,
    LoginView,
    MeView,
    PatientAppointmentsView,
    PatientMeView,
    PaymentDetailView,
    RegisterView,
)

# ── Router ───────────────────────────────────────────────────
router = DefaultRouter()
router.register(r"clinics",      ClinicViewSet,      basename="clinic")
router.register(r"doctors",      DoctorViewSet,      basename="doctor")
router.register(r"appointments", AppointmentViewSet, basename="appointment")
router.register(r"drugs",        DrugViewSet,        basename="drug")

# ── URL Patterns ─────────────────────────────────────────────
urlpatterns = [

    # ── Auth ────────────────────────────────────────────────
    path("auth/register/",        RegisterView.as_view(),       name="auth-register"),
    path("auth/login/",           LoginView.as_view(),          name="auth-login"),
    path("auth/token/refresh/",   TokenRefreshView.as_view(),   name="auth-token-refresh"),
    path("auth/me/",              MeView.as_view(),             name="auth-me"),
    path("auth/change-password/", ChangePasswordView.as_view(), name="auth-change-password"),

    # ── Patient ──────────────────────────────────────────────
    path("patients/me/",               PatientMeView.as_view(),          name="patient-me"),
    path("patients/me/appointments/",  PatientAppointmentsView.as_view(), name="patient-appointments"),

    # ── Slots ────────────────────────────────────────────────
    path("slots/available/", AvailableSlotsView.as_view(), name="slots-available"),

    # ── Payment (không qua router vì không có list) ──────────
    path("payments/<uuid:pk>/", PaymentDetailView.as_view(), name="payment-detail"),

    # ── API Docs ─────────────────────────────────────────────
    # path("schema/", SpectacularAPIView.as_view(),                          name="schema"),
    # path("docs/",   SpectacularSwaggerView.as_view(url_name="schema"),     name="swagger-ui"),
    # path("redoc/",  SpectacularRedocView.as_view(url_name="schema"),       name="redoc"),

    # ── Router (clinics, doctors, appointments, drugs) ───────
    path("api/", include(router.urls)),
]

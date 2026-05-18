"""
MediFlow — config/settings/drf.py
===================================
Cấu hình Django REST Framework, JWT và drf-spectacular.
Import file này trong base.py:
    from config.settings.drf import *
"""

from datetime import timedelta

# ─────────────────────────────────────────────────────────────
# INSTALLED APPS cần thêm vào base.py
# ─────────────────────────────────────────────────────────────
DRF_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "rest_framework",
    "drf_spectacular",
    "corsheaders",
]

# ─────────────────────────────────────────────────────────────
# DJANGO REST FRAMEWORK
# ─────────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    # Authentication
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    # Permission mặc định: phải đăng nhập
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    # Pagination
    "DEFAULT_PAGINATION_CLASS": "api.views.StandardPagination",
    "PAGE_SIZE": 20,
    # Renderer — chỉ JSON trong production, thêm BrowsableAPI khi dev
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    # Parser
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.MultiPartParser",   # upload file
        "rest_framework.parsers.FormParser",
    ],
    # Throttling — chống brute force
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "30/minute",    # IP không đăng nhập
        "user": "200/minute",   # User đã đăng nhập
        "auth": "10/minute",    # Dùng cho login/register riêng
    },
    # Filter
    "DEFAULT_FILTER_BACKENDS": [
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    # Schema
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # Exception handler tùy chỉnh
    "EXCEPTION_HANDLER": "api.exceptions.custom_exception_handler",
    # Date/Time format
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "DATE_FORMAT": "%Y-%m-%d",
    "TIME_FORMAT": "%H:%M",
}

# ─────────────────────────────────────────────────────────────
# JWT SETTINGS (Simple JWT)
# ─────────────────────────────────────────────────────────────
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME":  timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS":  True,       # Refresh token mới sau mỗi lần dùng
    "BLACKLIST_AFTER_ROTATION": True,     # Blacklist token cũ
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
}

# ─────────────────────────────────────────────────────────────
# DRF SPECTACULAR (Swagger / OpenAPI 3)
# ─────────────────────────────────────────────────────────────
SPECTACULAR_SETTINGS = {
    "TITLE":       "MediFlow API",
    "DESCRIPTION": "Hệ thống quản lý phòng khám & đặt lịch khám bệnh.",
    "VERSION":     "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "SCHEMA_PATH_PREFIX": r"/api/",
    "SWAGGER_UI_SETTINGS": {
        "persistAuthorization": True,
        "displayRequestDuration": True,
    },
    "TAGS": [
        {"name": "auth",          "description": "Đăng ký, đăng nhập, JWT"},
        {"name": "clinics",       "description": "Phòng khám"},
        {"name": "doctors",       "description": "Bác sĩ"},
        {"name": "patients",      "description": "Bệnh nhân"},
        {"name": "slots",         "description": "Slot khám trống"},
        {"name": "appointments",  "description": "Lịch hẹn khám"},
        {"name": "drugs",         "description": "Danh mục thuốc"},
        {"name": "payments",      "description": "Thanh toán"},
    ],
}

# ─────────────────────────────────────────────────────────────
# CORS (corsheaders)
# ─────────────────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",    # React dev server
    "http://localhost:5173",    # Vite dev server
]
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "x-csrftoken",
    "x-requested-with",
]

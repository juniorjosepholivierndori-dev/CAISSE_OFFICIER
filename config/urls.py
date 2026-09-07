from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    path("accounts/", include(("apps.accounts.urls", "accounts"), namespace="accounts")),
    path("api/accounts/", include(("apps.accounts.urls", "accounts"), namespace="accounts_api")),
    path("api/operations/", include("apps.operations.urls")),

    path("", include("apps.dashboard.urls")),

    path(
        "api/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),

    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
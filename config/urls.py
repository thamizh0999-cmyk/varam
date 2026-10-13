
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.shortcuts import redirect

from clinical.views import DashboardLoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "accounts/login/",
        DashboardLoginView.as_view(),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path("registers/", include("registers.urls", namespace="registers")),
    path("", include("clinical.urls")),
]

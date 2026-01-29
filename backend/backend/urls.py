from chemicals.views import UserRegistrationView, index_view
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.utils import extend_schema
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# Decorate JWT views with tags
@extend_schema(tags=["Authentication"])
class TaggedTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(tags=["Authentication"])
class TaggedTokenRefreshView(TokenRefreshView):
    pass


urlpatterns = [
    path("", index_view, name="home"),
    path("admin/", admin.site.urls),
    # Authentication
    path("api/v1/auth/register/", UserRegistrationView.as_view(), name="register"),
    path(
        "api/v1/auth/token/",
        TaggedTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/v1/auth/token/refresh/",
        TaggedTokenRefreshView.as_view(),
        name="token_refresh",
    ),
    # API
    path("api/v1/", include("chemicals.urls")),
    # Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

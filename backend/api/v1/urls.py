from chemicals.views import ChemicalRenderView, UserRegistrationView
from django.urls import path
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


@extend_schema(tags=["Authentication"])
class TaggedTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(tags=["Authentication"])
class TaggedTokenRefreshView(TokenRefreshView):
    pass


urlpatterns = [
    # Authentication
    path("auth/register/", UserRegistrationView.as_view(), name="register"),
    path("auth/token/", TaggedTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TaggedTokenRefreshView.as_view(), name="token_refresh"),
    # Chemicals API
    path("answer/", ChemicalRenderView.as_view(), name="answer"),
]

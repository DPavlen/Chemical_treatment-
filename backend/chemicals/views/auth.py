from chemicals.serializers import UserRegistrationSerializer, UserSerializer
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class UserRegistrationView(APIView):
    """User registration endpoint."""

    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Authentication"],
        summary="Register a new user",
        description="Create a new user account. Returns user info on success.",
        request=UserRegistrationSerializer,
        responses={
            201: UserSerializer,
            400: {"description": "Validation error"},
        },
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                UserSerializer(user).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

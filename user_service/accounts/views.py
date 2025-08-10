from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    authentication_classes = []
    permission_classes = []


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")

        user = User.objects.filter(email=email).first()
        if user is not None and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            data = {
                "user": str(user),
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            return Response(data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

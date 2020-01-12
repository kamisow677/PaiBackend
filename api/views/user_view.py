from django.contrib.auth import login, authenticate, logout
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import UserRegisterSerializer, UserPasswordChangeSerializer, UserRetrieveUpdateSerializer, \
    UserDestroySerializer


class RegisterUserView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegisterSerializer


class RetrieveUpdateUserView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserRetrieveUpdateSerializer

    def get_object(self, queryset=None):
        return self.request.user


class PasswordChangeUserView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserPasswordChangeSerializer

    def get_object(self, queryset=None):
        return self.request.user


class DestroyUserView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserDestroySerializer

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.user is not None:
            logout(request)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

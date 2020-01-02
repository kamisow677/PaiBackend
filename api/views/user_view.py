from django.contrib.auth import login, authenticate, logout
from rest_framework.response import Response

from ..serializers import LocationSerializer
from rest_framework.views import APIView
from django.http import Http404, JsonResponse, HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication, status
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from ..serializers import UserProfileSerializer

# {
# "username":"user1",
# "password":"password"
# }
class LoginView(APIView):
    def post(self, request, format=None):
        data = request.data
        print(request.data)
        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)
        print(user)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse(status=status.HTTP_200_OK)
            else:
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        else:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = User.objects.get(username=request.user.username)
        print(user.password)
        authenticate(username=user.username, password=user.password)

        print(request.user.is_active)
        if request.user is not None:
            if request.user.is_active:
                logout(request)
                return HttpResponse(status=status.HTTP_200_OK)
            else:
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        else:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

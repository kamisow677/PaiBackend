from django.contrib.auth import login, authenticate, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404, JsonResponse, HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication, status
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from ..serializers import UserProfileSerializer


class LoginView(APIView):
    def post(self, request, format=None):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(status=status.HTTP_200_OK)
        else:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        if request.user is not None:
            logout(request)
            return HttpResponse(status=status.HTTP_200_OK)
        else:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

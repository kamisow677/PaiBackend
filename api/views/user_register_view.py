# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status, generics
from ..models import Location
from ..serializers import UserProfileSerializer
from rest_framework.views import APIView
from django.http import Http404
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated


class LocationUserRegister(generics.GenericAPIView):
    serializer_class = UserProfileSerializer

    def post(self, request, format=None):
        serializer = UserProfileSerializer(data=request.data)
        data = request.data;
        if serializer.is_valid():
            user = User.objects.create_user(data['username'], data['email'], data['password'])
            user.last_name = data['last_name'];
            user.first_name = data['first_name'];
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

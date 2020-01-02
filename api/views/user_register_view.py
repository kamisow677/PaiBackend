from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status, generics
from ..models import Location
from ..serializers import UserProfileSerializer
from rest_framework.views import APIView
from django.http import Http404, JsonResponse, HttpResponse
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated


class LocationUserRegister(generics.GenericAPIView):
    serializer_class = UserProfileSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.utils import json

from ..models import Location
from ..serializers import LocationSerializer
from django.core import serializers

from rest_framework.views import APIView
from django.http import Http404, JsonResponse, HttpResponse
from rest_framework.permissions import IsAuthenticated


class LocationUserList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LocationSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Location.objects.filter(user=user)

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title=title)
        longitude = self.request.query_params.get('longitude', None)
        if longitude is not None:
            queryset = queryset.filter(longitude=longitude)
        latitude = self.request.query_params.get('latitude', None)
        if latitude is not None:
            queryset = queryset.filter(longitude=latitude)
        description = self.request.query_params.get('description', None)
        if description is not None:
            queryset = queryset.filter(description=description)

        return queryset;

    def get(self, request, *args, **kwargs):
        serializer = LocationSerializer(self.get_queryset(), many=True)
        return JsonResponse(list(serializer.data), safe=False)

    def post(self, request, format=None):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            Location.objects.create(longitude=serializer.data['longitude'],
                                           title=serializer.data['title'],
                                           latitude=serializer.data['latitude'],
                                           description=serializer.data['description'],
                                           user=request.user)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


class LocationUserDetailList(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LocationSerializer

    def get_object(self, pk):
        try:
            return Location.objects.get(pk=pk)
        except Location.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        location = self.get_object(pk)
        serializer = LocationSerializer(location)
        return JsonResponse(serializer.data)

    def put(self, request, pk, format=None):
        location = self.get_object(pk)
        serializer = LocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        location = self.get_object(pk)
        location.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

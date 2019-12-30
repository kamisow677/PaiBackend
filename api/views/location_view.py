from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from ..models import Location
from ..serializers import LocationSerializer
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.permissions import IsAuthenticated


class LocationList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            Location.objects.create(
                title=serializer.data['title'],
                longitude=serializer.data['longitude'],
                latitude=serializer.data['latitude'],
                description=serializer.data['description'],
                user=request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class LocationDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Location.objects.get(pk=pk)
        except Location.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        location = self.get_object(pk)
        serializer = LocationSerializer(location)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        location = self.get_object(pk)
        serializer = LocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        location = self.get_object(pk)
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'DELETE', 'PUT'])
# def get_delete_update_locations(request, pk):
#     try:
#         loc = Location.objects.get(pk=pk)
#     except Location.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     # get details of a single locations
#     if request.method == 'GET':
#         serializer = LocationSerializer(loc)
#         return Response(serializer.data)
#     # delete a single locations
#     elif request.method == 'DELETE':
#         loc.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     # update details of a single locations
#     elif request.method == 'PUT':
#         serializer = LocationSerializer(loc, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'POST'])
# def get_post_locations(request):
#     # get all locations
#     if request.method == 'GET':
#         locations = Location.objects.all()
#         serializer = LocationSerializer(locations, many=True)
#         return Response(serializer.data)
#     # insert a new record for a locations
#     elif request.method == 'POST':
#         data = {
#             'longitude': request.data.get('longitude'),
#             'latitude': request.data.get('latitude')
#         }
#         serializer = LocationSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

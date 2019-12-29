from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Location
from .serializers import LocationSerializer


@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_locations(request, pk):
    try:
        loc = Location.objects.get(pk=pk)
    except Location.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get details of a single locations
    if request.method == 'GET':
        serializer = LocationSerializer(loc)
        return Response(serializer.data)
    # delete a single locations
    elif request.method == 'DELETE':
        loc.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    # update details of a single locations
    elif request.method == 'PUT':
        serializer = LocationSerializer(loc, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def get_post_locations(request):
    # get all locations
    if request.method == 'GET':
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)
    # insert a new record for a locations
    elif request.method == 'POST':
        data = {
            'position_x': request.data.get('position_x'),
            'position_y': request.data.get('position_y')
        }
        serializer = LocationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

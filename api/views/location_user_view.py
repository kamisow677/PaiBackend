# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status, generics
from ..models import Location
from ..serializers import LocationSerializer
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.permissions import IsAuthenticated


class LocationUserList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LocationSerializer
    def get_queryset(self):
        user = self.request.user
        queryset =  Location.objects.filter(user=user)

        position_x = self.request.query_params.get('position_x', None)
        if position_x is not None:
            queryset = queryset.filter(position_x=position_x)
        position_y = self.request.query_params.get('position_y', None)
        if position_y is not None:
            queryset = queryset.filter(position_x=position_y)
        description = self.request.query_params.get('description', None)
        if description is not None:
            queryset = queryset.filter(description=description)

        return queryset

    def post(self, request, format=None):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            user = Location.objects.create(position_x=serializer.data['position_x'], position_y=serializer.data['position_y']
                                           , description=serializer.data['description'], user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

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
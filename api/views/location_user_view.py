from django.http import Http404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..models import Location
from ..serializers import LocationSerializer


class ListCreateLocationView(generics.ListCreateAPIView):
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

        return queryset


class RetrieveUpdateDestroyLocationView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LocationSerializer

    def get_object(self):
        loc_id = self.kwargs.get(self.lookup_field)
        user = self.request.user
        try:
            return Location.objects.get(user=user, id=loc_id)
        except Location.DoesNotExist:
            raise Http404

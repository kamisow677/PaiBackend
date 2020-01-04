from django.http import Http404
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework.permissions import IsAuthenticated

from ..models import Photo, Location
from ..serializers import PhotoSerializer, PhotoListSerializer


class ListPhotoView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoListSerializer
    lookup_url_kwarg = "pk"

    def get_location(self):
        loc_id = self.kwargs.get(self.lookup_url_kwarg)
        user = self.request.user
        try:
            return Location.objects.get(user=user, id=loc_id)
        except Location.DoesNotExist:
            raise Http404

    def get_queryset(self):
        location = self.get_location()
        queryset = location.photos.all()
        return queryset


class CreatePhotoView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = PhotoSerializer


class PhotoView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoSerializer
    parser_classes = (MultiPartParser, JSONParser,)
    lookup_url_kwarg = "pk"

    def get_object(self):
        photo_id = self.kwargs.get(self.lookup_url_kwarg)
        user = self.request.user
        try:
            photo = Photo.objects.get(id=photo_id)
        except Photo.DoesNotExist:
            raise Http404
        if photo.location.user_id == user.id:
            return photo
        else:
            raise Http404

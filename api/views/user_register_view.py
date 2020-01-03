from rest_framework import status, generics
from django.http import JsonResponse, HttpResponse
from rest_framework import status, generics

from ..serializers import UserProfileSerializer


class LocationUserRegister(generics.GenericAPIView):
    serializer_class = UserProfileSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

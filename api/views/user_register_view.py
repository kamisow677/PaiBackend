from rest_framework import generics

from ..serializers import UserProfileSerializer


class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer

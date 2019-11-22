from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Location
from rest_framework import authentication
from django.contrib.auth.models import User

# class UserProfileSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     username = serializers.CharField(max_length=200, read_only=True)
#     email = serializers.EmailField(max_length=400, read_only=True)
#     first_name = serializers.CharField(max_length=200, read_only=True)
#     last_name = serializers.CharField(max_length=200, read_only=True)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'position_x', 'position_y', 'description')

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Location


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'title', 'longitude', 'latitude', 'description', 'photo')
        extra_kwargs = {'description': {'required': True}}

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super(LocationSerializer, self).create(validated_data)

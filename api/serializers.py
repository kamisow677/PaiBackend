from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Location, Photo


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True},}

    def create(self, validated_data):
        user = User(**validated_data)
        # Hash the user's password.
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'location', 'file',)


class PhotoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'file',)


class LocationSerializer(serializers.ModelSerializer):
    photos = PhotoListSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Location
        fields = ('id', 'title', 'longitude', 'latitude', 'description', 'photos')
        extra_kwargs = {'description': {'required': True}}

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super(LocationSerializer, self).create(validated_data)

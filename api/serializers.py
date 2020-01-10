from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Location, Photo


class UserPasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, max_length=128)
    new_password = serializers.CharField(required=True, max_length=128)

    def validate(self, data):
        # validate_password(value)
        # add here additional check for password strength if needed
        if not self.context['request'].user.check_password(data.get('password')):
            raise serializers.ValidationError({'password': 'Wrong password.'})
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        # make sure the user stays logged in
        update_session_auth_hash(self.context['request'], self.context['request'].user)
        instance.save()
        return instance

    def create(self, validated_data):
        pass

    @property
    def data(self):
        return {'Success': True}


class UserDestroySerializer(serializers.Serializer):
    password = serializers.CharField(required=True, max_length=128)

    def validate(self, data):
        if not self.context['request'].user.check_password(data.get('password')):
            raise serializers.ValidationError({'password': 'Wrong password.'})
        return data

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}, }

    def create(self, validated_data):
        user = User(**validated_data)
        # Hash the user's password.
        user.set_password(validated_data['password'])
        validated_data['password'] = user.password
        return super(UserRegisterSerializer, self).create(validated_data)


class UserRetrieveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


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

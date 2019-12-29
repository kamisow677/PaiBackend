import json

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Location
from ..serializers import LocationSerializer

# initialize the APIClient app
client = Client()


class GetAllLocationsUserTest(TestCase):
    """ Test module for GET all puppies API """

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='password')
        self.client.login(username='user1', password='password')

        Location.objects.create(position_x=3, position_y=5, description="desc1")
        Location.objects.create(position_x=6, position_y=7, description="desc2")


# TODO REPAIR
# def test_get_all_locations(self):
#     # get API response
#     self.client.login(username='user1', password='password')
#     response = self.client.get(reverse('user_locations_bezpk'))
#     # get data from db
#     locations = Location.objects.all()
#     serializer = LocationSerializer(locations, many=True)
#
#     self.assertEqual(response.data, serializer.data)
#     self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetSingleLocationUserTest(TestCase):
    """ Test module for GET single puppy API """

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='password')
        self.loc1 = Location.objects.create(
            position_x=1, position_y=3, description="desc1")
        self.loc2 = Location.objects.create(
            position_x=2, position_y=4, description="desc2")

    def test_get_valid_single_location(self):
        self.client.login(username='user1', password='password')
        response = self.client.get(reverse('user_locations_zpk', kwargs={'pk': self.loc1.pk}))
        location = Location.objects.get(pk=self.loc1.pk)
        serializer = LocationSerializer(location)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_location(self):
        self.client.login(username='user1', password='password')
        response = self.client.get(reverse('user_locations_zpk', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewLocationUserTest(TestCase):
    """ Test module for inserting a new puppy """

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='password')
        self.valid_payload = {
            'position_x': 1,
            'position_y': 2,
            'description': "plasd"
        }
        self.invalid_payload = {
            'position_y': 2
        }

    def test_create_valid_location(self):
        self.client.login(username='user1', password='password')
        response = self.client.post(
            reverse('user_locations_bezpk'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_location(self):
        self.client.login(username='user1', password='password')
        response = self.client.post(
            reverse('user_locations_bezpk'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleLocationUserTest(TestCase):
    """ Test module for updating an existing puppy record """

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='password')
        self.loc1 = Location.objects.create(position_x=1, position_y=3, description="desc1")
        self.loc2 = Location.objects.create(position_x=2, position_y=4, description="desc2")
        self.valid_payload = {
            'position_x': 1,
            'position_y': 5,
            'description': "desc"
        }
        self.invalid_payload = {
            'position_y': 2
        }

    def test_valid_update_location(self):
        self.client.login(username='user1', password='password')
        response = self.client.put(
            reverse('user_locations_zpk', kwargs={'pk': self.loc2.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_location(self):
        self.client.login(username='user1', password='password')
        response = self.client.put(
            reverse('user_locations_zpk', kwargs={'pk': self.loc2.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleLocationUserTest(TestCase):
    """ Test module for deleting an existing puppy record """

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='password')
        self.loc1 = Location.objects.create(position_x=1, position_y=3, description="desc1")
        self.loc2 = Location.objects.create(position_x=2, position_y=4, description="desc2")

    def test_valid_delete_location(self):
        self.client.login(username='user1', password='password')
        response = self.client.delete(reverse('user_locations_zpk', kwargs={'pk': self.loc2.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_delete_location(self):
        self.client.login(username='user1', password='password')
        response = self.client.delete(reverse('user_locations_zpk', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

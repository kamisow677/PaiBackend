import json

from django.contrib.auth.models import User
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Location
from ..serializers import LocationSerializer

# initialize the APIClient app
client = Client()


class PaiTestCase(TestCase):

    def setUp(self):
        self.loc1 = Location.objects.create(title='title1', longitude=1.1, latitude=0.0, description="desc1")
        self.loc2 = Location.objects.create(title='title2', longitude=2.2, latitude=3.3, description="desc2")
        self.user = User.objects.create_user(username='user1', password='password')
        self.client.login(username='user1', password='password')


# class GetAllLocationsUserTest(TestCase):
#
#     def setUp(self):
#         self.user = User.objects.create_user(username='user1', password='password')
#         self.client.login(username='user1', password='password')
#
#         Location.objects.create(title='title1', longitude=3, latitude=5, description="desc1")
#         Location.objects.create(title='title2', longitude=6, latitude=7, description="desc2")


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

class GetSingleLocationUserTest(PaiTestCase):

    def test_get_valid_single_location(self):
        response = self.client.get(reverse('user_locations_zpk', kwargs={'pk': self.loc1.pk}))
        location = Location.objects.get(pk=self.loc1.pk)
        serializer = LocationSerializer(location)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_location(self):
        response = self.client.get(reverse('user_locations_zpk', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewLocationUserTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='password')
        self.client.login(username='user1', password='password')

    def test_create_valid_location(self):
        valid_payload = {
            'title': 'title1',
            'longitude': 1,
            'latitude': 2,
            'description': "plasd"
        }
        valid_payload_empty_description = {
            'title': 'title1',
            'longitude': 1,
            'latitude': 2,
            'description': ""
        }

        self.helper_create_valid_location(valid_payload)
        self.helper_create_valid_location(valid_payload_empty_description)

    def helper_create_valid_location(self, valid_payload):
        response = self.client.post(
            reverse('user_locations_bezpk'),
            data=json.dumps(valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_location(self):
        no_title = {
            'longitude': 1,
            'latitude': 2,
            'description': "plasd"
        }
        no_longitude = {
            'title': 'title1',
            'latitude': 2,
            'description': "plasd"
        }
        no_latitude = {
            'title': 'title1',
            'longitude': 1,
            'description': "plasd"
        }
        no_description = {
            'title': 'title1',
            'longitude': 1,
            'latitude': 2
        }
        blank_title = {
            'title': '',
            'longitude': 1,
            'latitude': 2,
            'description': "plasd"
        }
        null_title = {
            'title': None,
            'longitude': 1,
            'latitude': 2,
            'description': "plasd"
        }
        null_longitude = {
            'title': 'title1',
            'longitude': None,
            'latitude': 2,
            'description': "plasd"
        }
        null_latitude = {
            'title': 'title1',
            'longitude': 1,
            'latitude': None,
            'description': "plasd"
        }
        null_description = {
            'title': 'title1',
            'longitude': 1,
            'latitude': 2,
            'description': None
        }

        self.helper_create_invalid_location(no_title)
        self.helper_create_invalid_location(no_longitude)
        self.helper_create_invalid_location(no_latitude)
        self.helper_create_invalid_location(no_description)
        self.helper_create_invalid_location(blank_title)
        self.helper_create_invalid_location(null_title)
        self.helper_create_invalid_location(null_longitude)
        self.helper_create_invalid_location(null_latitude)
        self.helper_create_invalid_location(null_description)

    def helper_create_invalid_location(self, invalid_payload):
        response = self.client.post(
            reverse('user_locations_bezpk'),
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleLocationUserTest(PaiTestCase):

    def test_valid_update_location(self):
        valid_payload = {
            'title': 'abc',
            'longitude': 11.11,
            'latitude': 22.22,
            'description': "abc"
        }
        empty_description = {
            'title': 'abc',
            'longitude': 11.11,
            'latitude': 22.22,
            'description': ""
        }
        title = {
            'title': 'abc'
        }
        longitude = {
            'longitude': 11.11
        }
        latitude = {
            'longitude': 11.11
        }
        description = {
            'description': "abc"
        }
        self.helper_valid_update_location(valid_payload)
        self.helper_valid_update_location(empty_description)
        self.helper_valid_update_location(longitude)
        self.helper_valid_update_location(title)
        self.helper_valid_update_location(description)
        self.helper_valid_update_location(latitude)

    def helper_valid_update_location(self, valid_payload):
        response = self.client.patch(
            reverse('user_locations_zpk', kwargs={'pk': self.loc2.pk}),
            data=json.dumps(valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_location(self):
        blank_title = {
            'title': '',
            'longitude': 11.11,
            'latitude': 22.22,
            'description': "abc"
        }
        null_title = {
            'title': None,
            'longitude': 11.11,
            'latitude': 22.22,
            'description': "abc"
        }
        null_longitude = {
            'title': 'abc',
            'longitude': None,
            'latitude': 22.22,
            'description': "abc"
        }
        null_latitude = {
            'title': 'abc',
            'longitude': 11.11,
            'latitude': None,
            'description': "abc"
        }
        null_description = {
            'title': 'abc',
            'longitude': 11.11,
            'latitude': 22.22,
            'description': None
        }
        self.helper_invalid_update_location(blank_title)
        self.helper_invalid_update_location(null_title)
        self.helper_invalid_update_location(null_longitude)
        self.helper_invalid_update_location(null_latitude)
        self.helper_invalid_update_location(null_description)

    def helper_invalid_update_location(self, invalid_payload):
        response = self.client.patch(
            reverse('user_locations_zpk', kwargs={'pk': self.loc2.pk}),
            data=json.dumps(invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleLocationUserTest(PaiTestCase):

    def test_valid_delete_location(self):
        response = self.client.delete(reverse('user_locations_zpk', kwargs={'pk': self.loc2.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_delete_location(self):
        response = self.client.delete(reverse('user_locations_zpk', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

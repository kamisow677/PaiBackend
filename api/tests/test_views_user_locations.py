import json
from json import loads

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from ..models import Location
from ..serializers import LocationSerializer

# initialize the APIClient app
client = Client()


class PaiTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.loc1 = Location.objects.create(title='title1', longitude=1.1, latitude=0.0, description="desc1",
                                            user=self.user1)
        self.loc2 = Location.objects.create(title='title2', longitude=2.2, latitude=3.3, description="desc2",
                                            user=self.user1)
        self.loc3 = Location.objects.create(title='title', longitude=4.4, latitude=5.5, description="desc",
                                            user=self.user2)
        self.loc4 = Location.objects.create(title='title', longitude=4.4, latitude=5.5, description="desc")
        self.client.login(username='user1', password='password')


class GetAllLocationsUserTest(PaiTestCase):

    def test_get_all_locations(self):
        locations = Location.objects.filter(user=self.user1.pk)
        serializer = LocationSerializer(locations, many=True)
        expected = serializer.data

        response = self.client.get(reverse('user_locations_bezpk'))
        actual = loads(response.content)

        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleLocationUserTest(PaiTestCase):

    def test_get_valid_single_location(self):
        location = Location.objects.get(pk=self.loc1.pk)
        serializer = LocationSerializer(location)
        expected = serializer.data

        response = self.client.get(reverse('user_locations_zpk', kwargs={'pk': self.loc1.pk}))
        actual = loads(response.content)

        self.assertEqual(expected, actual)
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
        actual = loads(response.content)
        self.assertEqual(valid_payload["title"], actual["title"])
        self.assertEqual(valid_payload["longitude"], actual["longitude"])
        self.assertEqual(valid_payload["latitude"], actual["latitude"])
        self.assertEqual(valid_payload["description"], actual["description"])
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
        partial_update_1 = {
            'title': 'abc'
        }
        partial_update_2 = {
            'description': "abc",
            'longitude': 11.11
        }
        response = self.helper_valid_update_location(valid_payload)
        actual = loads(response.content)
        self.assertEqual(valid_payload["title"], actual["title"])
        self.assertEqual(valid_payload["longitude"], actual["longitude"])
        self.assertEqual(valid_payload["latitude"], actual["latitude"])
        self.assertEqual(valid_payload["description"], actual["description"])

        response = self.helper_valid_update_location(empty_description)
        actual = loads(response.content)
        self.assertEqual(empty_description["description"], actual["description"])

        response = self.helper_valid_update_location(partial_update_1)
        actual = loads(response.content)
        self.assertEqual(partial_update_1["title"], actual["title"])

        response = self.helper_valid_update_location(partial_update_2)
        actual = loads(response.content)
        self.assertEqual(partial_update_2["description"], actual["description"])
        self.assertEqual(partial_update_2["longitude"], actual["longitude"])

    def helper_valid_update_location(self, valid_payload):
        response = self.client.patch(
            reverse('user_locations_zpk', kwargs={'pk': self.loc2.pk}),
            data=json.dumps(valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response

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
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertRaises(Location.DoesNotExist, Location.objects.get, id=self.loc2.pk)

    def test_invalid_delete_location(self):
        response = self.client.delete(reverse('user_locations_zpk', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

from django.test import TestCase
from ..models import Location


class LocationTest(TestCase):
    """ Test module for Puppy model """

    def setUp(self):
        Location.objects.create(
            longitude=1, latitude=3)
        Location.objects.create(
            longitude=2, latitude=4)

    def test_location(self):
        loc1 = Location.objects.get(longitude=1)
        loc2 = Location.objects.get(longitude=2)
        self.assertEqual(loc1.longitude, 1)
        self.assertEqual(loc2.longitude, 2)

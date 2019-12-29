from django.test import TestCase
from ..models import Location


class LocationTest(TestCase):
    """ Test module for Puppy model """

    def setUp(self):
        Location.objects.create(
            position_x=1, position_y=3)
        Location.objects.create(
            position_x=2, position_y=4)

    def test_location(self):
        loc1 = Location.objects.get(position_x=1)
        loc2 = Location.objects.get(position_x=2)
        self.assertEqual(loc1.position_x, 1)
        self.assertEqual(loc2.position_x, 2)

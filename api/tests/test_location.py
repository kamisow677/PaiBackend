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
        loca1 = Location.objects.get(position_x=1)
        loca2 = Location.objects.get(position_x=2)
        self.assertEqual(
            loca1.position_x , 1)
        self.assertEqual(
            loca2.position_x, 2)


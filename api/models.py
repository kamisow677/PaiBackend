from django.contrib.auth.models import User
from django.db import models


class Location(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __repr__(self):
        return f'title: {self.title}, longitude: {str(self.longitude)}, latitude: {str(self.latitude)}, description: {self.description}'


class Photo(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='photos')
    file = models.ImageField(upload_to='location_photos')

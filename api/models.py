from django.contrib.auth.models import User
from django.db import models


class Location(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    photo = models.ImageField(default='default.jpg', upload_to='location_photos')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __repr__(self):
        return f'title: {self.title}, longitude: {str(self.longitude)}, latitude: {str(self.latitude)}, description: {self.description}'

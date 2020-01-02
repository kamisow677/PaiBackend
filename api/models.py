from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Location(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __repr__(self):
        return f'title: {self.title}, longitude: {str(self.longitude)}, latitude: {str(self.latitude)}, description: {self.description}'

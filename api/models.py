from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    position_x = models.IntegerField()
    position_y = models.IntegerField()
    description = models.CharField(max_length=100, blank=True, default='')


    def __repr__(self):
        return 'postision X: ' + self.position_x + 'postision Y: ' + self.position_y + ' description: ' + self.description

# In your app's models.py file
from django.db import models
from django.contrib.auth.models import User


class BookAppointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    time_interval = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    gmeet_link = models.URLField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s appointment at {self.date_time}"

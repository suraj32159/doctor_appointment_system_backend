# In your app's models.py file
from django.db import models
from django.contrib.auth.models import User


class BookAppointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming appointments are associated with a user
    date_time = models.DateTimeField()  # Date and time of the appointment
    time_interval = models.CharField(max_length=100)
    location = models.CharField(max_length=100)  # Location of the appointment
    description = models.TextField(blank=True, null=True)  # Optional description

    # Add any other fields you need for your appointments

    def __str__(self):
        return f"{self.user.username}'s appointment at {self.date_time}"

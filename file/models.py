from django.db import models

class UserProfile(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    profile_photo = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.fname} {self.lname}"


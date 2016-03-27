from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profile_pic = models.ImageField(upload_to="img", blank=True, null=True)
    score = models.IntegerField(default=0)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


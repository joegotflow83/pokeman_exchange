from django.db import models
from django.contrib.auth.models import User

from taggit.managers import TaggableManager


class Vote(models.Model):
    username = models.CharField(max_length=32)

    def __str__(self):
        return self.username


class Answer(models.Model):
    user = models.ForeignKey(User)
    response = models.TextField()
    like = models.IntegerField(default=0)
    votes = models.ManyToManyField(Vote)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-like']


class Post(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    body = models.TextField()
    tags = TaggableManager()
    answers = models.ManyToManyField(Answer)
    created = models.DateTimeField(auto_now_add=True)

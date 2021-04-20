from django.db import models

from .validators import validate_participants


class Song(models.Model):
    name = models.CharField(max_length=100, blank=False)
    duration = models.PositiveIntegerField(blank=False)
    uploaded_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Podcast(models.Model):
    name = models.CharField(max_length=100, blank=False)
    duration = models.PositiveIntegerField(blank=False)
    uploaded_time = models.DateTimeField(auto_now_add=True)
    host = models.CharField(max_length=100)
    participants = models.CharField(max_length=1040, validators=[validate_participants])

    def __str__(self):
        return self.name


class Audiobook(models.Model):
    title = models.CharField(max_length=100, blank=False)
    author = models.CharField(max_length=100, blank=False)
    narrator = models.CharField(max_length=100, blank=False)
    duration = models.PositiveIntegerField(blank=False)
    uploaded_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

from django.contrib.auth.models import User

from django.contrib.gis.db import models


class Trail(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)
    path = models.LineStringField()

    def __str__(self):
        return self.name


class Review(models.Model):
    trail = models.ForeignKey(Trail, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} on {self.trail.name}'

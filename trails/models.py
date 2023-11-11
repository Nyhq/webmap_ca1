from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.gis.geos import LineString
from django.contrib.gis.db.models.functions import Length


class Trail(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)
    path = models.LineStringField()  # Keep as LineString for a path
    length = models.FloatField(editable=False)  # Auto-calculated length

    def save(self, *args, **kwargs):
        # Ensure the path is a loop by checking if start and end points are the same
        if self.path and isinstance(self.path, LineString):
            self.length = round(self.path.length, 2)  # Calculate and round the length
        super(Trail, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Review(models.Model):
    trail = models.ForeignKey(Trail, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()  # Rating out of 5, for example
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} on {self.trail.name}'

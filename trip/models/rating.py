from django.db import models


class Rating(models.Model):
    rating = models.FloatField()
    review = models.TextField()
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    destination = models.ForeignKey('Destination', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
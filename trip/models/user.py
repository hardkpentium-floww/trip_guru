from django.db import models


class User(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    phone_no = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    blacklist = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

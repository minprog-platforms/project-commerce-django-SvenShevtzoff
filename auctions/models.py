from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=64)
    image_link = models.CharField(max_length=1024)

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=1024)

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()

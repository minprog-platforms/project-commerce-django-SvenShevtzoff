from typing import List
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watching = models.ManyToManyField("Listing", blank=True, related_name="watched_by")

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=64)
    image_link = models.CharField(blank=True, max_length=1024)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}, {self.description}, {self.starting_bid}, {self.image_link}"

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()

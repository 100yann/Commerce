from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass



class Listing(models.Model):
    title = models.CharField(max_length=100)


class ListingDetails(models.Model):
    CATEGORY_CHOICES = [
                ('1', 'Fashion'),
                ('2', 'Home'),
                ('3', 'Toys'),
                ('4', 'Electronics'),
                ('5', 'Books'),
                ('6', 'Misc'),
                ]

    descr = models.CharField(max_length=1000)
    starting_bid = models.PositiveIntegerField()
    img = models.URLField(blank=True)
    category = models.CharField(max_length=50, blank=True, choices=CATEGORY_CHOICES)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass



class Listing(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


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
    date_added = models.DateField(blank=True)


    def __str__(self):
        return f'{self.descr}, {self.starting_bid}, {self.img}, {self.category}'
    

    def save(self, *args, **kwargs):
        self.date_added = timezone.now()
        return super(ListingDetails, self).save(*args, **kwargs)


class Bids(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    highest_bid = models.PositiveIntegerField()
    bidder = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.highest_bid}, {self.bidder}'
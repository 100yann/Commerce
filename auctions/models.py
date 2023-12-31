from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=100)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='single_reference')
    watchlist = models.ManyToManyField(User, related_name='multiple_reference', null=True, blank=True)
    active = models.BooleanField(default=True)
    won_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='won_by', null=True)

    def __str__(self):
        watchlist_users = ', '.join([user.username for user in self.watchlist.all()])

        return f'{self.id}, {self.title}, {self.added_by}, {watchlist_users}, {self.active}'


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
    img = models.URLField(blank=True, max_length=1000)
    category = models.CharField(max_length=50, blank=True, choices=CATEGORY_CHOICES)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    date_added = models.DateField(blank=True)

    def __str__(self):
        return f'{self.listing},{self.descr}, {self.starting_bid}, {self.img}, {self.category}'
    

    def save(self, *args, **kwargs):
        self.date_added = timezone.now()
        return super(ListingDetails, self).save(*args, **kwargs)
    
    def is_active(self):
        return self.listing.active


class Bids(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    highest_bid = models.PositiveIntegerField()
    bidder = models.CharField(max_length=100)
    num_of_bids = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.listing}, {self.bidder}, {self.highest_bid}, {self.num_of_bids}'
    

class Comments(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.listing}, {self.user}, {self.content}, {self.timestamp}'
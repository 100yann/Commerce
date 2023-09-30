from django.contrib import admin
from .models import User, Listing, ListingDetails, Bids

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(ListingDetails)
admin.site.register(Bids)

# Register your models here.

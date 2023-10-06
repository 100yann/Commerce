from django.contrib import admin
from .models import User, Listing, ListingDetails, Bids, Comments

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(ListingDetails)
admin.site.register(Bids)
admin.site.register(Comments)

# Register your models here.

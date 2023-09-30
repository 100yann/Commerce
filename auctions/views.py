from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, ListingDetails, Bids
from django.forms import ModelForm
from django import forms
from django.contrib.auth.decorators import login_required




class NewListing(ModelForm):
    class Meta:
        model = Listing
        exclude = ('added_by', 'active',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }

class NewListingDetails(ModelForm):
    class Meta:
        model = ListingDetails
        exclude = ('listing',)
        widgets = {
            'descr': forms.Textarea(attrs={'class': 'form-control'}),
            'starting_bid': forms.NumberInput(attrs={'class': 'form-control'}),
            'img': forms.URLInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


def index(request):
    listings_details = ListingDetails.objects.select_related('listing').all()
    all_bids = Bids.objects.select_related('listing').all()
    return render(request, "auctions/index.html", {
        'listings': listings_details,
        'all_bids': all_bids
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    if request.method == 'POST':
        form1 = NewListing(request.POST)
        form2 = NewListingDetails(request.POST)
        if form1.is_valid() and form2.is_valid():
            listing_instance = form1.save(commit=False)
            user = request.user.id
            listing_instance.added_by = User.objects.get(id=user)
            listing_instance.save()

            listing_details_instance = form2.save(commit=False)
            listing_details_instance.listing = listing_instance
            listing_details_instance.save()

            bid_instance = Bids()
            bid_instance.listing = listing_instance
            bid_instance.bidder = request.user.username
            bid_instance.highest_bid = form2.cleaned_data['starting_bid']
            bid_instance.num_of_bids = 0
            bid_instance.save()
            
            return HttpResponseRedirect(reverse("index"))
        else:
            print(form1.errors, form2.errors)
    return render(request, "auctions/create_listing.html", {
        'form1': NewListing,
        'form2': NewListingDetails
    })
    
    
@login_required
def view_listing(request, listing_id, title):
    listing = Listing.objects.get(id=listing_id)
    get_listing_details = ListingDetails.objects.get(listing=listing_id)
    get_bid = Bids.objects.get(listing=listing_id)
    current_user = User.objects.get(pk=request.user.id)
    watchlist = current_user in listing.watchlist.all()
    print(listing)

    if request.method == "POST":
        if request.POST.get('save-bid') and request.POST.get('new_bid') != '':        
            new_bid = int(request.POST.get('new_bid'))
            if new_bid > get_bid.highest_bid:
                get_bid.highest_bid = new_bid
                get_bid.num_of_bids += 1
                user = request.user.username
                get_bid.bidder = user
                get_bid.save()
        elif request.POST.get('save-watchlist'):
            if watchlist == True:
                listing.watchlist.remove(current_user)
                watchlist = False
            else:
                listing.watchlist.add(current_user)
                watchlist = True
            listing.save()
        elif request.POST.get('close'):
            listing.active = False
            listing.save()
            print(listing)

    context = {
        'title': listing,
        'details': get_listing_details,
        'bids': get_bid,
        'watchlist': watchlist
        
        }

    return render(request, "auctions/view_listing.html", context)

@login_required
def watchlist(request):
    watched_listings = Listing.objects.filter(watchlist=request.user.id)
    all_listings = ListingDetails.objects.filter(listing__in=watched_listings)
    context = {
        'listings': all_listings
    }
    return render(request, 'auctions/watchlist.html', context)
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, ListingDetails
from django.forms import ModelForm
from django import forms


class NewListing(ModelForm):
    class Meta:
        model = Listing
        fields = '__all__'
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
    return render(request, "auctions/index.html", {
        'listings': listings_details
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


def create_listing(request):
    if request.method == 'POST':
        form1 = NewListing(request.POST)
        form2 = NewListingDetails(request.POST)
        if form1.is_valid() and form2.is_valid():
            listing_instance = form1.save()

            listing_details_instance = form2.save(commit=False)
            listing_details_instance.listing = listing_instance
            listing_details_instance.save()

            return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create_listing.html", {
        'form1': NewListing,
        'form2': NewListingDetails
    })
    
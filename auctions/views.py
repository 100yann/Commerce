from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, ListingDetails, Bids, Comments
from django.forms import ModelForm
from django import forms
from django.contrib.auth.decorators import login_required
from django.conf import settings





class NewListing(ModelForm):
    class Meta:
        model = Listing
        exclude = ('added_by', 'active', 'won_by', )
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
            'comments': forms.Textarea(attrs={'class': 'form-control comment'})
        }


def index(request):
    listings_details = ListingDetails.objects.select_related('listing').all()
    all_bids = Bids.objects.select_related('listing').all()
    all_listings = zip(listings_details, all_bids)
    listings_won = len(Listing.objects.filter(won_by = request.user.id))
    return render(request, "auctions/index.html", {
        'all_listings': all_listings,
        'listings_won': listings_won
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

@login_required(login_url="/login")
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
            if listing_details_instance.img == '':
                listing_details_instance.img = settings.STATIC_URL + '/images/default.jpg'
            listing_details_instance.save()

            bid_instance = Bids()
            bid_instance.listing = listing_instance
            bid_instance.bidder = request.user.username
            bid_instance.highest_bid = form2.cleaned_data['starting_bid']
            bid_instance.num_of_bids = 0
            bid_instance.save()
            
            return HttpResponseRedirect(f'view/{listing_instance.id}')
        else:
            print(form1.errors, form2.errors)
    listings_won = Listing.objects.filter(won_by=request.user.id)
    return render(request, "auctions/create_listing.html", {
        'form1': NewListing,
        'form2': NewListingDetails,
        'listings_won': len(listings_won)

    })
    
    
@login_required(login_url="/login")
def view_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    get_listing_details = ListingDetails.objects.get(listing=listing_id)
    get_bid = Bids.objects.get(listing=listing_id)
    current_user = User.objects.get(pk=request.user.id)
    watchlist = current_user in listing.watchlist.all()
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
            listing_winner = User.objects.get(username=get_bid.bidder)
            listing.won_by = listing_winner
            listing.save()
        elif request.POST.get('comment'):
            comment = request.POST['new-comment']
            if comment != '':
                new_comment = Comments.objects.create(listing=listing, 
                                                    user=current_user,
                                                    content=comment)
                new_comment.save()

    all_comments = Comments.objects.filter(listing=listing).order_by('-timestamp')
    listings_won = len(Listing.objects.filter(won_by = request.user.id))
    context = {
        'title': listing,
        'details': get_listing_details,
        'bids': get_bid,
        'watchlist': watchlist,
        'listings_won': listings_won,
        'comments_form': NewListingDetails,
        'comments': all_comments
        }

    return render(request, "auctions/view_listing.html", context)

@login_required(login_url="/login")
def watchlist(request):
    watched_listings = Listing.objects.filter(watchlist=request.user.id)
    listing_details = ListingDetails.objects.filter(listing__in=watched_listings)
    bids = Bids.objects.filter(listing__in=watched_listings)
    all_listings = zip(listing_details, bids)
    listings_won = Listing.objects.filter(won_by=request.user.id)
    context = {
        'all_listings': all_listings,
        'listings_won': len(listings_won)
     
    }
    return render(request, 'auctions/watchlist.html', context)

@login_required(login_url="/login")
def categories(request, category):
    categories = ListingDetails.CATEGORY_CHOICES
    curr_category = 'All'
    for i in categories:
        if i[1] == category.title():
            curr_category = i[1]
            index = i[0]
            listing_details = ListingDetails.objects.filter(category=index)
            all_bids = Bids.objects.filter(listing__listingdetails__category=index)
            break
    if curr_category == 'All':
        listing_details = ListingDetails.objects.select_related('listing').all()
        all_bids = Bids.objects.select_related('listing').all()
    all_listings = zip(listing_details, all_bids)
    listings_won = Listing.objects.filter(won_by=request.user.id)

    return render(request, 'auctions/categories.html', {
        'categories': categories,
        'all_listings': all_listings,
        'curr_category': curr_category,
        'listings_won': len(listings_won)

    })

@login_required
def listings_won(request):
    listings_won = Listing.objects.filter(won_by=request.user.id)
    listing_details = ListingDetails.objects.filter(listing__in=listings_won)
    bids = Bids.objects.filter(listing__in=listings_won)
    all_listings = zip(listing_details, bids)
    context = {
        'all_listings': all_listings,
        'listings_won': len(listings_won)
    }
    return render(request, 'auctions/listings_won.html', context)
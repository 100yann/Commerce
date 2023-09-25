from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User


def index(request):
    return render(request, "auctions/index.html")


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


categories = (
    (0, ''),
    (1, 'Fashion'),
    (2, 'Home'),
    (3, 'Toys'),
    (4, 'Electronics')
)

class NewForm(forms.Form):
    title = forms.CharField(required=True)    
    descr = forms.CharField(required=True)
    starting_bid = forms.IntegerField(required=True)
    image = forms.URLField(required=False)
    category = forms.ChoiceField(choices=(categories))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



def create_listing(request):
    if request.method == 'POST':
        form = NewForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            print(clean_data)
            field_data = {}
            field_names = ['title', 'descr', 'starting_bid', 'image', 'category']
            
            for name in field_names:
                field_data[name] = clean_data[name]
            field_data['category'] = categories[int(field_data['category'])][1]

    return render(request, "auctions/create_listing.html", {
        'form': NewForm
    })
    
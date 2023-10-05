from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("view/<int:listing_id>/<str:title>", views.view_listing, name="view"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories/<str:category>", views.categories, name="categories"),
    path("listings_won", views.listings_won, name="listings_won")
]

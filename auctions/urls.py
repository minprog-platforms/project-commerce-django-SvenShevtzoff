from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"), 
    path("create", views.create, name="create"), 
    path("listing/<str:requested_title>", views.listing, name="listing"), 
    path("delete/<str:listing_title>", views.delete, name="delete"), 
    path("watchlist", views.watchlist, name="watchlist")
]

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid
from .forms import NewBidForm, NewListingForm, NewCommentForm

def get_highest_bid(bids):
    highest = 0
    for bid in bids:
        if bid.amount > int(highest):
            highest = int(bid.amount)
    
    return highest
    

def index(request):
    context = {}
    if request.method == 'POST':
        form = NewListingForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()

    for listing in Listing.objects.all():
        if listing.bids.all():
            listing.starting_bid = get_highest_bid(listing.bids.all())
            listing.save()
    
    context["listings"] = Listing.objects.filter(active=True).all()

    return render(request, "auctions/index.html", context)


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
def create(request):
    form = NewListingForm()
    return render(request, "auctions/create.html", {
        "form": form
    })

def listing(request, requested_title):
    context = {}
    listing = Listing.objects.filter(title=requested_title).first()

    if request.method == 'POST':
        if 'bid'in request.POST:
            if request.user.is_authenticated:
                bid_form = NewBidForm(request.POST, prefix='bid')
                if bid_form.is_valid():
                    bid = bid_form.cleaned_data["amount"]
                    if int(bid) > int(listing.starting_bid) and int(bid) > get_highest_bid(listing.bids.all()):
                        bid_form = bid_form.save(commit=False)
                        bid_form.user = request.user
                        bid_form.listing = Listing.objects.filter(title=requested_title).first()
                        bid_form.save()
                    else:
                        context["bid_message"] = "Your bid is not high enough"
            else:
                context["bid_message"] = "You need to be logged in to place a bid"

        elif 'comment' in request.POST:
            if request.user.is_authenticated:
                comment_form = NewCommentForm(request.POST, prefix='comment')
                if comment_form.is_valid():
                    comment_form = comment_form.save(commit=False)
                    comment_form.user = request.user
                    comment_form.listing = Listing.objects.filter(title=requested_title).first()
                    comment_form.save()
            else:
                context["comment_message"] = "You need to be logged in to comment on this listing"
        
        elif 'watch' in request.POST:
            if request.user.is_authenticated:
                request.user.watching.add(listing)



    if request.user == listing.user:
        context["remove_listing"] = 1
    
    if listing.bids.all():
            listing.starting_bid = get_highest_bid(listing.bids.all())
            listing.save()

    if not listing.bids:
        top_bid_user = Bid.objects.filter(amount=get_highest_bid(listing.bids.all())).first().user
        
        if request.user == top_bid_user and listing.active == False:
            context["winning_message"] = "You have won this listing"

    context["bid_form"] = NewBidForm(prefix='bid')
    context["comment_form"] = NewCommentForm(prefix='comment')
    context["listing"] = listing
    if listing.image_link != "":
        context["image_link"] = listing.image_link
    
    context["bids"] = listing.bids.all()
    context["comments"] = listing.comments.all()
    return render(request, "auctions/listing.html", context)

def delete(request, listing_title):
    context = {}
    
    listing_to_deactivate = Listing.objects.filter(title=listing_title).first()
    listing_to_deactivate.active = False
    listing_to_deactivate.save()

    for listing in Listing.objects.all():
        if listing.bids.all():
            listing.starting_bid = get_highest_bid(listing.bids.all())
            listing.save()
    
    context["listings"] = Listing.objects.filter(active=True).all()

    return render(request, "auctions/index.html", context)

def watchlist(request):
    
    for listing in Listing.objects.all():
        if listing.bids.all():
            listing.starting_bid = get_highest_bid(listing.bids.all())
            listing.save()
        
    watched_listings = request.user.watching.all()
    
    return render(request, "auctions/watchlist.html", {
        "watched_listings": watched_listings
    })

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import Comment, User, Listing, Bid

class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image_link']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}), 
            'description': forms.Textarea(attrs={'class': 'form-control'}), 
            'starting_bid': forms.TextInput(attrs={'class': 'form-control'}), 
            'image_link': forms.TextInput(attrs={'class': 'form-control'})
        }

class NewBidForm(forms.ModelForm):
    amount = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter amount'}), label="")

    class Meta:
        model = Bid
        fields = ['amount']

        widgets = {
            'amount': forms.TextInput(attrs={'class': 'form-control'})
        }

class NewCommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter comment here', 'rows': 1, 'cols': 85}), label="")

    class Meta:
        model = Comment
        fields = ['comment']

        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control'})
        }
    

def index(request):
    if request.method == 'POST':
        form = NewListingForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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
def create(request):
    form = NewListingForm()
    return render(request, "auctions/create.html", {
        "form": form
    })

def listing(request, requested_title):
    context = {}
    if request.method == 'POST':
        if 'bid'in request.POST:
            if request.user.is_authenticated:
                bid_form = NewBidForm(request.POST, prefix='bid')
                if bid_form.is_valid():
                    bid_form = bid_form.save(commit=False)
                    bid_form.user = request.user
                    bid_form.listing = Listing.objects.filter(title=requested_title).first()
                    bid_form.save()
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

    context["bid_form"] = NewBidForm(prefix='bid')
    context["comment_form"] = NewCommentForm(prefix='comment')
    listing = Listing.objects.filter(title=requested_title).first()
    context["listing"] = listing
    context["bids"] = listing.bids.all()
    context["comments"] = listing.comments.all()
    return render(request, "auctions/listing.html", context)
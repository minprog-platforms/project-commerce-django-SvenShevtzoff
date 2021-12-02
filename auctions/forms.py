from django import forms
from .models import Comment, Listing, Bid


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
    class Meta:
        model = Bid
        fields = ['amount']
        labels = { "amount": ""}

        widgets = {
            'amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter amount'})
        }

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        labels = {"comment": ""}

        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'class': 'form-control', 'placeholder': 'Enter comment here', 'rows': 1, 'cols': 85})
        }
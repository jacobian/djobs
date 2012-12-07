from django import forms
from .models import JobListing

class JobListingForm(forms.ModelForm):
    class Meta(object):
        model = JobListing
        fields = ['title', 'description', 'compensation', 'location', 'remote']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-block-level'}),
            'description': forms.Textarea(attrs={'class': 'input-block-level'}),
            'compensation': forms.TextInput(attrs={'class': 'input-block-level'}),
            'location': forms.TextInput(attrs={'class': 'input-block-level'}),
        }

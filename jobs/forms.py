from django import forms
from .models import JobListing

class JobListingForm(forms.ModelForm):
    class Meta(object):
        model = JobListing
        fields = ['title', 'description', 'compensation', 'location', 'remote',
                  'employer_name', 'employer_website', 'contact_name', 'contact_email']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-block-level'}),
            'description': forms.Textarea(attrs={'class': 'input-block-level'}),
            'compensation': forms.TextInput(attrs={'class': 'input-block-level'}),
            'location': forms.TextInput(attrs={'class': 'input-block-level'}),
            'employer_name': forms.TextInput(attrs={'class': 'input-block-level'}),
            'employer_website': forms.TextInput(attrs={'class': 'input-block-level'}),
            'contact_name': forms.TextInput(attrs={'class': 'input-block-level'}),
            'contact_email': forms.TextInput(attrs={'class': 'input-block-level'}),
        }

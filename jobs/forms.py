from django import forms

from taggit.forms import TagWidget

from .models import JobListing


class JobListingForm(forms.ModelForm):
    class Meta(object):
        model = JobListing
        fields = ['title', 'description', 'skills', 'compensation',
                  'location', 'location_latitude', 'location_longitude',
                  'remote', 'employer_name', 'employer_website',
                  'contact_name', 'contact_email']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-block-level'}),
            'description': forms.Textarea(attrs={'class': 'input-block-level'}),
            'skills': TagWidget(attrs={'class': 'input-block-level'}),
            'compensation': forms.TextInput(attrs={'class': 'input-block-level'}),
            'location': forms.TextInput(attrs={'class': 'input-block-level'}),
            'location_latitude': forms.HiddenInput(),
            'location_longitude': forms.HiddenInput(),
            'employer_name': forms.TextInput(attrs={'class': 'input-block-level'}),
            'employer_website': forms.TextInput(attrs={'class': 'input-block-level'}),
            'contact_name': forms.TextInput(attrs={'class': 'input-block-level'}),
            'contact_email': forms.TextInput(attrs={'class': 'input-block-level'}),
        }


class SearchForm(forms.Form):
    DISTANCES = (
        ('', '-----------'),
        ('50', '50 km'),
        ('100', '100 km'),
        ('1000', '1000 km'),
    )
    query = forms.CharField(widget=forms.TextInput(attrs={
                'class': 'search-query input-block-level',
                'placeholder': 'Search'}), required=False)
    distance = forms.ChoiceField(choices=DISTANCES, required=False)
    longitude = forms.FloatField(widget=forms.HiddenInput, required=False)
    latitude = forms.FloatField(widget=forms.HiddenInput, required=False)

from django.contrib import admin
from .models import JobListing

admin.site.register(JobListing,
    list_display = ('title', 'employer_name', 'status', 'created'),
    list_filter = ('status',),
    ordering = ('-created',),
)

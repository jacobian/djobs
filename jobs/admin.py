from django.contrib import admin
from .models import Employer, JobListing

admin.site.register(Employer,
    list_display = ('name', 'email', 'company_name'),
)

admin.site.register(JobListing,
    list_display = ('title', 'employer', 'status', 'created'),
    list_filter = ('status',),
    ordering = ('-created',),
)

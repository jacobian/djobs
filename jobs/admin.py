from django.contrib import admin

from .models import JobListing


class JobListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer_name', 'status', 'created')
    list_filter = ('status',)
    ordering = ('-created',)


admin.site.register(JobListing, JobListingAdmin)

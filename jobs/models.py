from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Employer(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=500)
    email = models.EmailField(max_length=500)
    company_name = models.CharField(max_length=500)
    company_website = models.URLField(blank=True)

    def __unicode__(self):
        return self.company_name

class JobListing(models.Model):
    employer = models.ForeignKey(Employer, related_name='listings')
    title = models.CharField(max_length=500, help_text='Title of the job - e.g. "Intern", "Software Developer", "CTO", etc.')
    description = models.TextField(help_text='Full job description. Markdown is allowed.')
    compensation = models.CharField(max_length=500, blank=True, help_text='Salary/compensation range (optional)')
    location = models.CharField(max_length=500, help_text='Where is the job located?')
    created = models.DateTimeField(default=timezone.now)

    REMOTE_YES = "yes"
    REMOTE_MAYBE = "maybe"
    REMOTE_NO = "no"
    REMOTE_CHOICES = (
        (REMOTE_YES, "yes"),
        (REMOTE_MAYBE, "negotiable"),
        (REMOTE_NO, "no (on-site only)"),
    )
    remote = models.CharField('Remote work allowed?', max_length=20, choices=REMOTE_CHOICES, default=REMOTE_MAYBE)

    STATUS_DRAFT = "draft"
    STATUS_ACTIVE = "active"
    STATUS_ARCHIVED = "archived"
    STATUS_REMOVED = "removed"
    STATUS_CHOICES = (
        (STATUS_DRAFT, "draft"),
        (STATUS_ACTIVE, "active"),
        (STATUS_ARCHIVED, "archived"),
        (STATUS_REMOVED, "removed")
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)

    def __unicode__(self):
        return self.title

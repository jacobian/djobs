from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from taggit.managers import TaggableManager


class JobListing(models.Model):
    creator = models.ForeignKey(User, related_name='job_listings')
    created = models.DateTimeField(default=timezone.now)

    # Job info
    title = models.CharField(max_length=500, help_text='Title of the job - e.g. "Intern", "Software Developer", "CTO", etc.')
    description = models.TextField(help_text='Full job description. Markdown is allowed.')
    compensation = models.CharField(max_length=500, blank=True, help_text='Salary/compensation range (optional)')
    location = models.CharField(max_length=500, help_text='Where is the job located?')
    skill_set = TaggableManager('Skills', help_text='Expected skill set (comma separated).')

    # Is remote work allowd?
    REMOTE_YES = "yes"
    REMOTE_MAYBE = "maybe"
    REMOTE_NO = "no"
    REMOTE_CHOICES = (
        (REMOTE_YES, "yes"),
        (REMOTE_MAYBE, "negotiable"),
        (REMOTE_NO, "no (on-site only)"),
    )
    remote = models.CharField('Remote work allowed?', max_length=20, choices=REMOTE_CHOICES, default=REMOTE_MAYBE)

    # Company info
    employer_name = models.CharField(max_length=500)
    employer_website = models.URLField(blank=True)

    # Contact info
    contact_name = models.CharField(max_length=200)
    contact_email = models.EmailField(max_length=500,
        help_text="Applicants will use this email to contact you. Your email will be protected by a CAPTCHA.")

    # Statuses: when a post is initially created it'll be draft, only visible
    # to the user who created it. Once they hit "publish" it becomes active.
    # Jobs that are filled or otherwise "done" can be archived by the creator.
    # The "removed" status is for admins to take spam etc.
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


class Flag(models.Model):
    job = models.ForeignKey(JobListing, related_name='flags')
    when = models.DateTimeField(default=timezone.now)
    cleared = models.BooleanField(default=False)

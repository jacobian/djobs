from django.contrib import messages
from django.core import urlresolvers
from django.db.models import Q
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from braces.views import LoginRequiredMixin
from .models import JobListing
from .forms import JobListingForm

class JobQuerysetMixin(object):
    """
    Auth'd users see their own postings; everyone else only sees "active" ones.
    """
    def get_queryset(self):
        q = Q(status=JobListing.STATUS_ACTIVE)
        if self.request.user.is_authenticated():
            q |= Q(creator=self.request.user)
        return self.model.objects.filter(q).order_by('-created')

class JobList(JobQuerysetMixin, ListView):
    """
    List of all published jobs.
    """
    model = JobListing
    template_name = "jobs/index.html"
    context_object_name = 'jobs'

class MyListings(LoginRequiredMixin, JobList):
    """
    "My listings" page.
    """
    template_name = "jobs/mine.html"

    def get_queryset(self):
        return self.request.user.job_listings.all()

class JobDetail(JobQuerysetMixin, DetailView):
    """
    Individual job listing view.
    """
    model = JobListing
    template_name = "jobs/detail.html"
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        return super(JobDetail, self).get_context_data(
            user_can_edit = (self.object.creator == self.request.user)
        )

class JobEditMixin(object):
    """
    Common helper for job create/edit.

    Provides:
        * success messages
        * redirect to the job detail on success
    """
    model = JobListing
    form_class = JobListingForm

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return super(JobEditMixin, self).form_valid(form)

    def get_success_url(self):
        return urlresolvers.reverse("job_detail", args=(self.object.id,))

class JobCreate(LoginRequiredMixin, JobEditMixin, CreateView):
    """
    Create a new job listing.
    """
    template_name = "jobs/create.html"
    success_message = "Your job listing has been saved as a draft."

    def get_form_kwargs(self):
        kwargs = super(JobCreate, self).get_form_kwargs()
        kwargs['instance'] = JobListing(creator=self.request.user, status=JobListing.STATUS_DRAFT)
        return kwargs

class JobEdit(LoginRequiredMixin, JobEditMixin, UpdateView):
    """
    Edit an existing job.

    Naturally only the person who created a job can edit it again.
    """
    template_name = "jobs/edit.html"
    success_message = "Your job listing has been updated."

    def get_queryset(self):
        return self.request.user.job_listings.all()

class ChangeJobStatus(LoginRequiredMixin, View):
    """
    Abstract class to change a job's status; see the concrete implentations below.
    """
    def post(self, request, pk):
        job = get_object_or_404(request.user.job_listings, pk=pk)
        job.status = self.new_status
        job.save()
        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return redirect('job_detail', job.id)

class PublishJob(ChangeJobStatus):
    new_status = JobListing.STATUS_ACTIVE
    success_message = "Your job listing has been published."

class ArchiveJob(ChangeJobStatus):
    new_status = JobListing.STATUS_ARCHIVED
    success_message = "Your job listing has been archived and is no longer public."

class Login(TemplateView):
    template_name = "login.html"

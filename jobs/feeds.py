from django.contrib.syndication.views import Feed
from django.contrib.markup.templatetags.markup import markdown
from django.core import urlresolvers
from .models import JobListing

class JobFeed(Feed):
    title = "Jobs for Djangonauts"
    link = "/"
    description = "Latest jobs posted at djobs.herokuapp.com"

    def items(self):
        qs = JobListing.objects.filter(status=JobListing.STATUS_ACTIVE)
        qs = qs.order_by('-created')
        return qs[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return markdown(item.description, 'safe')

    def item_link(self, item):
        return urlresolvers.reverse('job_detail', args=[item.id])

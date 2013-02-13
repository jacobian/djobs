from haystack import indexes
from .models import JobListing


class JobIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField()
    description = indexes.CharField()
    created = indexes.DateTimeField()
    location = indexes.CharField()
    location_coordinates = indexes.LocationField()
    skill = indexes.MultiValueField()

    def prepare_location_coordinates(self, obj):
        if obj.location_latitude and obj.location_longitude:
            return '%s,%s' % (obj.location_latitude, obj.location_longitude)
        else:
            return

    def prepare_skill(self, obj):
        return [t.name for t in obj.skills.all()]

    def get_model(self):
        return JobListing

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(status=JobListing.STATUS_ACTIVE)

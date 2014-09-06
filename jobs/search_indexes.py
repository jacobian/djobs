from haystack import indexes
from .models import JobListing


class JobIndex(indexes.SearchIndex, indexes.Indexable):
    # Ugly trick to ignore the document=True requirement by haystack, just let
    # elasticsearch do the right thing :)
    _all = indexes.CharField(document=True, indexed=False, stored=False)

    title = indexes.CharField(model_attr='title', boost=1.125, stored=False)
    description = indexes.CharField(model_attr='description', stored=False)

    location = indexes.CharField(model_attr='location', stored=False)
    location_coordinates = indexes.LocationField(stored=False)
    skill = indexes.MultiValueField(stored=False)

    def get_updated_field(self):
        return 'updated'

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

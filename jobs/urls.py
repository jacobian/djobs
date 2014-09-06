from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views
from . import feeds

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',                     views.JobList.as_view(),     name='job_list'),
    url(r'^new/$',                 views.JobCreate.as_view(),   name='job_create'),
    url(r'^mine/$',                views.MyListings.as_view(),  name='job_list_mine'),
    url(r'^(?P<pk>\d+)/$',         views.JobDetail.as_view(),   name='job_detail'),
    url(r'^(?P<pk>\d+)/edit/$',    views.JobEdit.as_view(),     name='job_edit'),
    url(r'^(?P<pk>\d+)/publish/$', views.PublishJob.as_view(),  name='job_publish'),
    url(r'^(?P<pk>\d+)/archive/$', views.ArchiveJob.as_view(),  name='job_archive'),
    url(r'^(?P<pk>\d+)/flag/$',    views.FlagJob.as_view(),     name='job_flag'),
    url(r'^search/$',              views.SearchView.as_view(),  name='job_search'),
    url(r'^feed/$',                feeds.JobFeed(),             name='job_feed'),
    url(r'^login/$',               views.Login.as_view(),       name='login'),
    url(r'^flags/$',               views.ReviewFlags.as_view(), name='review_flags'),
    url(r'^logout/$',              'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'',        include('social_auth.urls')),
)

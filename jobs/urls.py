from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from . import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',                     views.JobList.as_view(),    name='job_list'),
    url(r'^new/$',                 views.JobCreate.as_view(),  name='job_create'),
    url(r'^mine/$',                views.MyListings.as_view(), name='job_list_mine'),
    url(r'^(?P<pk>\d+)/$',         views.JobDetail.as_view(),  name='job_detail'),
    url(r'^(?P<pk>\d+)/edit/$',    views.JobEdit.as_view(),    name='job_edit'),
    url(r'^(?P<pk>\d+)/publish/$', views.PublishJob.as_view(), name='job_publish'),
    url(r'^(?P<pk>\d+)/archive/$', views.ArchiveJob.as_view(), name='job_archive'),
    url(r'^admin/',                include(admin.site.urls)),
)

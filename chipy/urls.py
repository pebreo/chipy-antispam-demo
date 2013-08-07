from django.conf.urls import patterns, url

from chipy import views

urlpatterns = patterns('',

    # /chipy/
    url(r'^$',views.index,name='index'),

    # /chipy/rsvp/
    url(r'^rsvp/$',views.rsvp,name='rsvp'),

    # /chipy/rsvp_list
    url(r'^rsvp_list/$',views.RsvpListView.as_view(),name='rsvp_list'),

    # e.g. /chipy/page/about
    url(r'^page/(?P<page_name>\w+)/$',views.message_page,name='message_page'),



)
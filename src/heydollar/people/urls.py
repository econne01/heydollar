from django.conf.urls import patterns, include, url
from heydollar.people.views import PeopleListView

urlpatterns = patterns('',
    url(r'^people', PeopleListView.as_view(template_name='people.html'), name='people_list'),
)

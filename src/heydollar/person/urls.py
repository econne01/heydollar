from django.conf.urls import patterns, include, url
from heydollar.person.views import PersonListView

urlpatterns = patterns('',
    url(r'^people', PersonListView.as_view(template_name='people.html'), name='people_list'),
)

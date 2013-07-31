from django.conf.urls import patterns, include, url
from heydollar.account.views import AccountListView

urlpatterns = patterns('',
    url(r'^accounts$', AccountListView.as_view(template_name='accounts.html'), name='account_list'),
)

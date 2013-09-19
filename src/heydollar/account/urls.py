from django.conf.urls import patterns, include, url
from heydollar.account.views import AccountListView, AccountCreateView

urlpatterns = patterns('',
    url(r'^$', AccountListView.as_view(template_name='accounts.html'), name='account_list'),
    url(r'^add$', AccountCreateView.as_view(template_name='account_form.html'), name='account_form'),
)

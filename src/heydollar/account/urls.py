from django.conf.urls import patterns, include, url
from heydollar.account import views

urlpatterns = patterns('',
    url(r'^$', views.AccountListView.as_view(template_name='account_list.html'), name='account_list'),
    url(r'^add$', views.AccountCreateView.as_view(template_name='account_form.html'), name='account_form'),
    url(r'^institution/$', views.FinancialInstitutionListView.as_view(template_name='financialinstitution_list.html'), name='financial_institution_list'),
    url(r'^institution/add$', views.FinancialInstitutionCreateView.as_view(), name='financialinstitution_form'),
)

from django.conf.urls import patterns, include, url
from heydollar.views import CategoryListView, TransactionListView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'heydollar.views.index', name='index'),
    url(r'^categories$', CategoryListView.as_view(template_name='categories.html'), name='category_list'),
    url(r'^history$', TransactionListView.as_view(template_name='transaction_history.html'), name='transaction_list'),
)

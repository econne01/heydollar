from django.conf.urls import patterns, include, url
from heydollar.spending.views import CategoryListView, TransactionListView

urlpatterns = patterns('',
    url(r'^categories$', CategoryListView.as_view(template_name='categories.html'), name='category_list'),
    url(r'^history$', TransactionListView.as_view(template_name='transaction_history.html'), name='transaction_list'),
    url(r'^upload/$', 'heydollar.spending.views.upload_history', name='upload_history'),
)
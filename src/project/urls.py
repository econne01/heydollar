from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'heydollar.views.index', name='index'),
    url(r'^balances/$', 'heydollar.views.balance_sheet_summary', name='balance_summary'),
    url(r'^account/', include('heydollar.account.urls')),
    url(r'^people/', include('heydollar.people.urls')),
    url(r'^spending/', include('heydollar.spending.urls')),
)

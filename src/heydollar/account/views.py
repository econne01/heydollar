from django.views.generic.list import ListView
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from heydollar.account.models import Account

class AccountListView(ListView):
    model = Account

class AccountCreateView(CreateView):
    model = Account
    fields = ['description', 'type', 'institution']

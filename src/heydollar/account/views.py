from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from heydollar.account.models import Account, FinancialInstitution
from heydollar.account.forms import AccountForm

class AccountListView(ListView):
    model = Account

class AccountCreateView(CreateView):
    model = Account
    form_class = AccountForm
    success_url=reverse_lazy('account_list')
    #fields = ['description', 'type', 'institution']
    
    def get(self, request, *args, **kwargs):
        ret = super(AccountCreateView, self).get(request, *args, **kwargs)
        return ret

class AccountUpdateView(UpdateView):
    model = Account
    success_url=reverse_lazy('account_list')
    #fields = ['description', 'type', 'institution']

class FinancialInstitutionListView(ListView):
    model = FinancialInstitution

class FinancialInstitutionCreateView(CreateView):
    model = FinancialInstitution
    success_url=reverse_lazy('financial_institution_list')
    fields = ['name']

from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from heydollar.account.models import Account, AccountNameMap, FinancialInstitution
from heydollar.account.forms import AccountForm

class AccountListView(ListView):
    model = Account

class AccountCreateView(CreateView):
    model = Account
    form_class = AccountForm
    success_url=reverse_lazy('account_list')
    
    def get_form(self, form_class):
        form = super(AccountCreateView, self).get_form(form_class)
        if 'account_name' in self.request.GET:
            form.initial['mapped_name'] = self.request.GET['account_name']
        return form

    def post(self, request, *args, **kwargs):
        response = super(AccountCreateView, self).post(request, *args, **kwargs)
        if self.object is not None:
            map_obj = AccountNameMap(
                account=self.object,
                name=self.request.POST['mapped_name'],
                user_id=self.request.POST['owner']
            )
            map_obj.save()
        return response

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

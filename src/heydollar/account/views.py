from django.views.generic.list import ListView
from heydollar.account.models import Account

class AccountListView(ListView):
    model = Account
    

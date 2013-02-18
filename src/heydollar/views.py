from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from heydollar.models import TransactionType, AccountType, Account, Category, Transaction 

def index(request):
    test_var = 'This string is a test variable'
    context = {'var': test_var}
    return render(request, 'heydollar_index.html', context)

class CategoryListView(ListView):
    model = Category
    
    def get_queryset(self):
        qs = super(CategoryListView, self).get_queryset()
        return qs.order_by('name')
    
    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        return context
    
class TransactionListView(ListView):
    model = Transaction
    
    def get_queryset(self):
        qs = super(TransactionListView, self).get_queryset()
        return qs.order_by('date', 'description')
    
    def get_context_data(self, **kwargs):
        context = super(TransactionListView, self).get_context_data(**kwargs)
        return context
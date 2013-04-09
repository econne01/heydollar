from django.views.generic.list import ListView
from heydollar.spending.models import Category, Transaction

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
        return qs.order_by('post_date', 'description')
    
    def get_context_data(self, **kwargs):
        context = super(TransactionListView, self).get_context_data(**kwargs)
        return context    

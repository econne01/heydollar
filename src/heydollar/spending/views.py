from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from heydollar.spending.models import Category, Transaction
from heydollar.spending.utils import MintFileUploader

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

def upload_history(request):
    if request.method == 'POST': # The form has been submitted
        # @todo: Validate the file input
        input_file = request.FILES['uploadHistoryInput']
        uploader = MintFileUploader()
        uploader.upload(input_file)
        return HttpResponseRedirect('/') # Redirect after POST

    return HttpResponseRedirect('/') # Redirect after POST
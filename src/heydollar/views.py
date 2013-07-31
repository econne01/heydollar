from datetime import datetime
from django.shortcuts import render

def index(request):
    test_var = 'This string is a test variable'
    context = {'var': test_var}
    return render(request, 'heydollar_index.html', context)

def balance_sheet_summary(request):
    balances = {
        'avail_cash': 100,
        'short_term_saving': 200,
        'long_term_saving': 300,
        'debt': 400,
    }
    context = balances
    context['end_date'] = datetime.today()
    return render(request, 'balance_summary.html', context)
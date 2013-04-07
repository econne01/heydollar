from django.shortcuts import render

def index(request):
    test_var = 'This string is a test variable'
    context = {'var': test_var}
    return render(request, 'heydollar_index.html', context)


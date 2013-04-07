from django.views.generic.list import ListView
from heydollar.people.models import People

class PeopleListView(ListView):
    model = People
    

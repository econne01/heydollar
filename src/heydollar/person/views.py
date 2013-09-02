from django.views.generic.list import ListView
from heydollar.person.models import Person

class PersonListView(ListView):
    model = Person
    

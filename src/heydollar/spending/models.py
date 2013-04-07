from django.db import models
from heydollar.account.models import Account

class TransactionType(models.Model):
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.name
    
class Transaction(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account = models.ForeignKey(Account)
    type = models.ForeignKey(TransactionType)
    category = models.ForeignKey(Category)
    description = models.CharField(max_length=128)
    orig_description = models.CharField(max_length=128)
    notes = models.TextField(blank=True)
    
    def __unicode__(self):
        return '%s (%s, %s)' % (self.description, self.date, self.amount)

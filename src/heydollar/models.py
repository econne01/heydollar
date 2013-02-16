from django.db import models

class TransactionType(models.Model):
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.name
    
class AccountType(models.Model):
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.name
    
class FinancialInstitution(models.Model):
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.name
    
class Account(models.Model):
    description = models.CharField(max_length=50)
    institution = models.ForeignKey(FinancialInstitution)
    type = models.ForeignKey(AccountType)
    login_user = models.CharField(max_length=50, blank=True)
    login_password = models.CharField(max_length=50, blank=True)
    
    def __unicode__(self):
        return self.description
    
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

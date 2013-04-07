from django.db import models
from heydollar.people.models import People

class AccountType(models.Model):
    BASE_SIGN_CHOICES = (
        (-1, 'Negative'),
        (1, 'Positive')
    )
    name = models.CharField(max_length=50)
    base_sign = models.IntegerField(choices=BASE_SIGN_CHOICES, default=1)
    
    def __unicode__(self):
        return self.name
    
class FinancialInstitution(models.Model):
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.name
    
class Account(models.Model):
    description = models.CharField(max_length=100)
    institution = models.ForeignKey(FinancialInstitution)
    type = models.ForeignKey(AccountType)
    owner = models.ForeignKey(People)
    login_user = models.CharField(max_length=50, blank=True, default='')
    login_password = models.CharField(max_length=50, blank=True, default='')
    
    def __unicode__(self):
        return self.description

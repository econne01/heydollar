from django.db import models
from heydollar.person.models import Person

class AccountType(models.Model):
    BASE_SIGN_CHOICES = (
        (-1, 'Negative'),
        (1, 'Positive')
    )
    name = models.CharField(unique=True, max_length=50)
    base_sign = models.IntegerField(choices=BASE_SIGN_CHOICES, default=1)

    def __unicode__(self):
        return self.name
    
class FinancialInstitution(models.Model):
    name = models.CharField(unique=True, max_length=50)
    
    def __unicode__(self):
        return self.name
    
class Account(models.Model):
    description = models.CharField(max_length=100)
    institution = models.ForeignKey(FinancialInstitution)
    type = models.ForeignKey(AccountType)
    owner = models.ForeignKey(Person)
    login_user = models.CharField(max_length=50, blank=True, default='')
    login_password = models.CharField(max_length=50, blank=True, default='')

    class Meta:
        unique_together = (('description', 'institution', 'type', 'owner'),)

    def __unicode__(self):
        return self.description

class AccountNameMap(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(Person) # Why is user here? To distinguish between the owner of the MINT acct (this uer) and ACCOUNT?
    account = models.ForeignKey(Account)
    
    class Meta:
        unique_together = (('user', 'account'),)

    def __unicode__(self):
        return self.name

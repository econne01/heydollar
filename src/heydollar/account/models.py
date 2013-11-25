from django.db import models
from heydollar.person.models import Person

class FinancialInstitution(models.Model):
    name = models.CharField(unique=True, max_length=50)

    def __unicode__(self):
        return self.name

class Account(models.Model):
    TYPE_CHOICES = (
        ('CHECKING', 'CHECKING'),
        ('SAVING', 'SAVING'),
        ('PERSONAL INVESTMENT', 'PERSONAL INVESTMENT'),
        ('RETIREMENT INVESTMENT', 'RETIREMENT INVESTMENT'),
        ('CREDIT CARD', 'CREDIT CARD'),
    )
    DEBIT_SIGN_CHOICES = (
        (-1, 'Decrease Account Value'),
        (1, 'Increase Account Value')
    )
    description = models.CharField(max_length=100)
    institution = models.ForeignKey(FinancialInstitution)
    type = models.CharField(max_length=31, choices=TYPE_CHOICES)
    debit_sign = models.IntegerField(choices=DEBIT_SIGN_CHOICES, default=-1)
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

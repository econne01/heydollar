from django.db import models
from heydollar.account.models import Account
from heydollar.people.models import People

class TransactionType(models.Model):
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', null=True, blank=True)
    
    def __unicode__(self):
        return self.name
    
class PurposeTag(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey('PurposeTagType')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    def __unicode__(self):
        return self.name
    
class PurposeTagType(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True)
    
    def __unicode__(self):
        return self.name

class Transaction(models.Model):
    ''' Core model for the personal finance data schema
    Mint.com aggregates several of these input fields by default, but some require a bit more explanation
    @field post_date: the default date listed by the financial institution online source
    @field transacted_date: optional override date (of purchase/transaction). User input.
    @field type: whether the transaction should add or subtract from account's total value (assuming all accounts
        either have zero or positive value)
    @field purpose_tags: a way to group similar transactions (ie, "Aruba Vacation" or "Kitchen remodelling")
    @field transacted_by: optional override for account__owner. For example, wife buys shoes on husband's card or
        son buys plane ticket on mom's card.
    '''
    post_date = models.DateField()
    transacted_date = models.DateField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account = models.ForeignKey(Account)
    type = models.ForeignKey(TransactionType)
    category = models.ForeignKey(Category)
    description = models.CharField(max_length=128)
    orig_description = models.CharField(max_length=128)
    notes = models.TextField(blank=True)
    purpose_tags = models.ManyToManyField(PurposeTag, null=True, blank=True)
    transacted_by = models.ForeignKey(People, null=True, blank=True)
    
    def __unicode__(self):
        return '%s (%s, %s)' % (self.description, self.date, self.amount)

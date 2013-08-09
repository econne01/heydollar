from django.test import TestCase
from heydollar.account import models as account_models
from heydollar.people import models as people_models
from heydollar.spending import models as spending_models

class HeydollarBaseTestCase(TestCase):

    def create_account(self, **kwargs):
        ''' Create a test instance of an Account object
        '''
        self.confirm_prerequisite_objects(
            account_models.FinancialInstitution,
            account_models.AccountType,
            people_models.People,
        )
        data = {
            'description': 'Test Account Description',
            'institution': account_models.FinancialInstitution.objects.get(pk=1),
            'type': account_models.AccountType.objects.get(pk=1),
            'owner': people_models.People.objects.get(pk=1),
        }
        data.update(kwargs)
        instance = account_models.Account(**data)
        instance.save()
        return instance

    def create_accountnamemap(self, **kwargs):
        ''' Create a test instance of an AccountNameMap object
        '''
        self.confirm_prerequisite_objects(
            account_models.Account,
            people_models.People,
        )
        data = {
            'name': 'Test Account Name Map',
            'account': account_models.Account.objects.get(pk=1),
            'owner': people_models.People.objects.get(pk=1),
        }
        data.update(kwargs)
        instance = account_models.AccountNameMap(**data)
        instance.save()
        return instance

    def confirm_prerequisite_objects(self, *args):
        ''' Confirm the listed Object Classes have at least one existing instance, else create one
        '''
        for object_cls in args:
            if object_cls.objects.count() == 0:
                create_method = getattr(self, 'create_' + object_cls.__name__.lower())
                create_method()

    def create_accounttype(self, **kwargs):
        ''' Create test instance of AccountType
        '''
        data = {
            'name': 'Test Account Type',
        }
        data.update(kwargs)
        instance = account_models.AccountType(**data)
        instance.save()
        return instance

    def create_financialinstitution(self, **kwargs):
        ''' Create test instance of FinancialInstitution
        '''
        data = {
            'name': 'Test Financial Institution',
        }
        data.update(kwargs)
        instance = account_models.FinancialInstitution(**data)
        instance.save()
        return instance

    def create_transactiontype(self, **kwargs):
        ''' Create test instance of TransactionType
        '''
        data = {
            'name': 'Test Transaction Type',
        }
        data.update(kwargs)
        instance = spending_models.TransactionType(**data)
        instance.save()
        return instance

    def create_category(self, **kwargs):
        ''' Create test instance of Category
        '''
        data = {
            'name': 'Test Category',
        }
        data.update(kwargs)
        instance = spending_models.Category(**data)
        instance.save()
        return instance

    def create_people(self, **kwargs):
        ''' Create test instance of People
        '''
        data = {
            'first_name': 'Test First',
            'last_name': 'Test Last',
            'birthdate': '1990-01-01',
            'gender': people_models.People.GENDER_CHOICES[0][0],
        }
        data.update(kwargs)
        instance = people_models.People(**data)
        instance.save()
        return instance

    def create_transaction(self, **kwargs):
        ''' Create a test instance of an Transaction object
        '''
        self.confirm_prerequisite_objects(
            account_models.Account,
            spending_models.TransactionType,
            spending_models.Category,
        )
        data = {
            'post_date': '2013-01-01',
            'amount': 123.45,
            'account': account_models.Account.objects.get(pk=1),
            'type': spending_models.TransactionType.objects.get(pk=1),
            'category': spending_models.Category.objects.get(pk=1),
            'description': 'Test Description',
            'orig_description': 'Test Original Description',
        }
        data.update(kwargs)
        instance = spending_models.Transaction(**data)
        instance.save()
        return instance

from django.test import TestCase
from heydollar.spending.utils import MintFileUploader
from heydollar.account import models as account_models
from heydollar.people import models as people_models
from heydollar.spending import models as spending_models

class TestUploadMintHistoryTask(TestCase):
    ''' Test the upload Mint.com history (csv file) process
    '''

    def setUp(self):
        super(TestUploadMintHistoryTask, self).setUp()
        # Create necessary foreign key objects
        self.txn_type = spending_models.TransactionType(name='debit')
        self.category = spending_models.Category(name='Groceries')
        self.financial_institution = account_models.FinancialInstitution(name='National Institution')
        self.account_type = account_models.AccountType(name='Checking', base_sign=1)
        self.person = people_models.Person(
            first_name='Ericson',
            last_name='Connelly',
            birthdate='1999-12-31'
        )
        self.account = account_models.Account(
            description = 'Official Heydollar Test Name',
            institution = self.financial_institution,
            type = self.account_type,
            owner = self.person
        )
        self.account_map = account_models.AccountNameMap(name='Mint easy to read name', user=self.person, account=self.account)

    def prepare_csv_file_row(self):
        ''' Create a sample row of data from the default csv Mint history file download
        '''
        return {
            MintFileUploader.file_fields.date                   : '01/01/2013',
            MintFileUploader.file_fields.description            : 'Some Description goes here',
            MintFileUploader.file_fields.original_description   : 'The Original Description -- often hard to read',
            MintFileUploader.file_fields.amount                 : '123.45',
            MintFileUploader.file_fields.transaction_type       : self.txn_type.name,
            MintFileUploader.file_fields.category               : self.category.name,
            MintFileUploader.file_fields.account                : self.account_map.name,
        }

    def test_can_map_download_file_row_data_to_database_spending_entry_object(self):
        ''' The map function should convert csv file format to a DB entry, with foreign key django objects
        '''
        uploader = MintFileUploader()
        db_data = uploader.map_row_to_db_format(self.prepare_csv_file_row())
        # Test all fields properly converted to new data format and new labels
        self.assertEqual(db_data[uploader.file_map[uploader.file_fields.transaction_type]], self.txn_type)
        self.assertEqual(db_data[uploader.file_map[uploader.file_fields.category]], self.category)
        self.assertEqual(db_data[uploader.file_map[uploader.file_fields.account]], self.account)
        

    def test_can_map_date_format_yyyy_mm_dd(self):
        ''' If the mint history file has dates formatted as YYYY-MM-DD, they will be read by mapper
        '''
        self.download_row_data[MintFileUploader.file_fields.date] = '2013-04-30'
        uploader = MintFileUploader()
        db_data = uploader.map_row_to_db_format(self.prepare_csv_file_row())
        self.assertEqual(db_data[uploader.file_map[uploader.file_fields.account]], '2013-04-30')

    def test_can_insert_a_new_db_row_from_history_data(self):
        ''' The uploader can insert a record to database after mapping the CSV history row data
        '''
        uploader = MintFileUploader()
        db_data = uploader.map_row_to_db_format(self.download_row_data)
        txn_cnt = spending_models.Transaction.objects.count()
        uploader.insert_update(db_data)
        self.assertEqual(spending_models.Transaction.objects.count(), txn_cnt+1)


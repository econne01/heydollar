import os
from autofixture.base import AutoFixture
from django.test import TestCase
from django.conf import settings

from heydollar import exceptions
from heydollar.spending.utils import MintFileUploader
from heydollar.account import models as account_models
from heydollar.person import models as person_models
from heydollar.spending import models as spending_models

class TestUploadMintHistoryTask(TestCase):
    ''' Test the upload Mint.com history (csv file) process
    '''

    def setUp(self):
        super(TestUploadMintHistoryTask, self).setUp()
        self.uploader = MintFileUploader()
        # Create necessary foreign key objects
        self.txn_type = AutoFixture(spending_models.TransactionType).create_one()
        self.category = AutoFixture(spending_models.Category).create_one()
        person = AutoFixture(person_models.Person).create_one()
        account = AutoFixture(account_models.Account, generate_fk=True).create_one()
        
        self.account_map = account_models.AccountNameMap(
            name='Account Map Name',
            user=person,
            account=account
        )

    def tearDown(self):
        ''' Remove any test files as needed
        '''
        super(TestUploadMintHistoryTask, self).tearDown()
        filename = 'FakeFileNameExample.txt'
        filename = os.path.abspath(os.path.sep.join([settings.PROJECT_PATH, filename]))
        if os.path.exists(filename):
            os.remove(filename)


    def prepare_default_upload_file_data(self):
        ''' Helper function to create a default sample row of data  
            from the default csv Mint history file download
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

    #---- TEST FILE INPUT ----#
    def test_will_throw_error_on_dne_file_input_to_uploader(self):
        ''' Must throw exception if input file to Uploader does not exist
        '''
        filename = 'FakeFileNameExample.txt'
        filename = os.path.abspath(os.path.sep.join([settings.PROJECT_PATH, filename]))
        self.assertFalse(os.path.exists(filename))

        # A file that DNE throws error
        self.assertRaises(
            exceptions.HeydollarInvalidUploadFile,
            self.uploader.upload,
            filename
        )

    def test_will_throw_error_on_bad_format_file_input_to_uploader(self):
        ''' Must throw exception if input file to Uploader has unexpected format
        '''
        filename = 'FakeFileNameExample.txt'
        filename = os.path.abspath(os.path.sep.join([settings.PROJECT_PATH, filename]))
        self.assertFalse(os.path.exists(filename))
        
        # Write unexpected column headers and data
        ofile = open(filename, 'w')
        ofile.write('\t'.join(['Header 1', 'Header 2']) + '\n')
        ofile.write('\t'.join(['String data', 'Other string']) + '\n')
        ofile.close()
        self.assertTrue(os.path.exists(filename))
        # Invalid file format must throw error
        self.assertRaises(
            exceptions.HeydollarInvalidUploadFile,
            self.uploader.upload,
            filename
        )
        self.assertEqual(1,2)

    def can_map_download_file_row_data_to_database_spending_entry_object(self):
        ''' The map function should convert csv file format to a DB entry, with foreign key django objects
        '''
        db_data = uploader.map_row_to_db_format(self.prepare_default_upload_file_data())
        # Test all fields properly converted to new data format and new labels
        self.assertEqual(db_data[uploader.file_map[uploader.file_fields.transaction_type]], self.txn_type)
        self.assertEqual(db_data[uploader.file_map[uploader.file_fields.category]], self.category)
        self.assertEqual(db_data[uploader.file_map[uploader.file_fields.account]], self.account)
        

    def can_map_date_format_yyyy_mm_dd(self):
        ''' If the mint history file has dates formatted as YYYY-MM-DD, they will be read by mapper
        '''
        self.download_row_data[MintFileUploader.file_fields.date] = '2013-04-30'
        uploader = MintFileUploader()
        db_data = uploader.map_row_to_db_format(self.prepare_default_upload_file_data())
        self.assertEqual(db_data[uploader.file_map[uploader.file_fields.account]], '2013-04-30')

    def can_insert_a_new_db_row_from_history_data(self):
        ''' The uploader can insert a record to database after mapping the CSV history row data
        '''
        uploader = MintFileUploader()
        db_data = uploader.map_row_to_db_format(self.download_row_data)
        txn_cnt = spending_models.Transaction.objects.count()
        uploader.insert_update(db_data)
        self.assertEqual(spending_models.Transaction.objects.count(), txn_cnt+1)


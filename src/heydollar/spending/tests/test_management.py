import os, datetime, decimal
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
    fake_filename = 'FakeFileNameExample.txt'

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
        self.account_map.save()

    def tearDown(self):
        ''' Remove any test files as needed
        '''
        super(TestUploadMintHistoryTask, self).tearDown()
        filename = os.path.abspath(os.path.sep.join([settings.PROJECT_PATH, self.fake_filename]))
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
            MintFileUploader.file_fields.notes                  : ''
        }

    #---- TEST FILE INPUT ----#
    def test_will_throw_error_on_dne_file_input_to_uploader(self):
        ''' Must throw exception if input file to Uploader does not exist
        '''
        filename = os.path.abspath(os.path.sep.join([settings.PROJECT_PATH, self.fake_filename]))
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
        filename = os.path.abspath(os.path.sep.join([settings.PROJECT_PATH, self.fake_filename]))
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

    def test_can_parse_upload_file_date_column_to_date_object(self):
        ''' Must be able to convert a date string in upload file to date object
        '''
        upload_data = self.prepare_default_upload_file_data()
        # Test parsing of format MM/DD/YYYY
        upload_data[self.uploader.file_fields.date] = '04/30/2013'
        db_data = self.uploader.map_row_to_db_format(upload_data)
        self.assertEqual(db_data[self.uploader.field_map[self.uploader.file_fields.date]], '2013-04-30')

    def test_can_parse_upload_file_description_field_including_delimiter_to_string(self):
        ''' Must be able to convert a string object in upload file to string, even
            if it contains a '\t' or other delimiter character
        '''
        upload_data = self.prepare_default_upload_file_data()
        # Prepare string with delimiter
        test_string = 'A test with \t tabs'
        upload_data[self.uploader.file_fields.description] = '"' + test_string + '"'
        # Write the test data to a file
        filename = os.path.abspath(os.path.sep.join([settings.PROJECT_PATH, self.fake_filename]))
        ofile = open(filename, 'w')
        ofile.write('\t'.join(upload_data.keys()) + '\n')
        ofile.write('\t'.join([upload_data[k] for k in upload_data.keys()]) + '\n')
        ofile.close()
        # Upload the test data to database
        self.uploader.upload(filename)
        # Filter for the uploaded Txn from database
        txn = spending_models.Transaction.objects.order_by('-pk')[0]
        self.assertEqual(txn.description, test_string)

    def test_can_parse_upload_file_amount_field_to_decimal(self):
        ''' Must be able to convert an amount string to decimal
        '''
        upload_data = self.prepare_default_upload_file_data()
        test_amount = decimal.Decimal(102.34)
        upload_data[self.uploader.file_fields.amount] = str(test_amount)
        db_data = self.uploader.map_row_to_db_format(upload_data)
        self.assertEqual(db_data[self.uploader.field_map[self.uploader.file_fields.amount]], test_amount)

    def test_can_parse_upload_file_category_field_to_new_category_object(self):
        ''' Must be able to convert category string to a new Category data object
            if none exists
        '''
        upload_data = self.prepare_default_upload_file_data()
        test_name = 'A New Category'
        # Confirm this is a new Category
        self.assertEqual(spending_models.Category.objects.filter(name=test_name).count(), 0)

        upload_data[self.uploader.file_fields.category] = test_name
        db_data = self.uploader.map_row_to_db_format(upload_data)
        # Confirm this new Category was created
        ctgy = spending_models.Category.objects.filter(name=test_name)[0]
        self.assertEqual(db_data[self.uploader.field_map[self.uploader.file_fields.category]], ctgy)

    def test_can_parse_upload_file_category_field_to_existing_category_object(self):
        ''' Must be able to convert category string to an existing Category data object
            if it exists
        '''
        upload_data = self.prepare_default_upload_file_data()
        test_amount = decimal.Decimal(102.34)
        upload_data[self.uploader.file_fields.amount] = str(test_amount)
        db_data = self.uploader.map_row_to_db_format(upload_data)
        self.assertEqual(db_data[self.uploader.field_map[self.uploader.file_fields.amount]], test_amount)

    def test_throw_error_for_upload_file_account_field_of_new_account_object(self):
        ''' Must throw Exception for an account string of an Account object that does not exist
        '''
        upload_data = self.prepare_default_upload_file_data()
        test_name = 'A New Account Name'
        # Confirm this is a new Account
        self.assertEqual(account_models.AccountNameMap.objects.filter(name=test_name).count(), 0)
        # Uploading with this account must throw an Error
        upload_data[self.uploader.file_fields.account] = test_name
        self.assertRaises(
            exceptions.HeydollarDoesNotExist,
            self.uploader.map_row_to_db_format,
            upload_data
        )

    def test_can_parse_upload_file_account_field_to_existing_account_object(self):
        ''' Must be able to convert account string to an existing Account data object
            if it exists
        '''
        upload_data = self.prepare_default_upload_file_data()
        test_account_map = self.account_map
        upload_data[self.uploader.file_fields.account] = test_account_map.name
        db_data = self.uploader.map_row_to_db_format(upload_data)
        self.assertEqual(db_data[self.uploader.field_map[self.uploader.file_fields.account]], test_account_map.account)

    def test_can_insert_new_upload_file_row_to_database(self):
        ''' Must insert record to database when uploading new transaction data
        '''
        upload_data = self.prepare_default_upload_file_data()
        # Write the test data to a file
        filename = os.path.abspath(os.path.sep.join([settings.PROJECT_PATH, self.fake_filename]))
        ofile = open(filename, 'w')
        ofile.write('\t'.join(upload_data.keys()) + '\n')
        ofile.write('\t'.join([upload_data[k] for k in upload_data.keys()]) + '\n')
        ofile.close()
        # Upload the test data to database
        txn_cnt = spending_models.Transaction.objects.count()
        self.uploader.upload(filename)
        self.assertEqual(spending_models.Transaction.objects.count(), txn_cnt+1)

    def test_can_update_existing_upload_file_row_to_database(self):
        ''' Must update record in database when uploading existing transaction data
        '''
        pass

    def test_must_insert_duplicate_upload_file_row_to_database(self):
        ''' Must insert new record to database when uploading duplicate transaction data
            (ie, the same unique record fields occur multiple times in one upload file)
        '''
        pass

    def test_can_differentiate_duplicate_database_entries_by_memo_field(self):
        ''' Must select proper database entry to update (as needed) by matching memo field
        '''
        pass

    def test_throw_error_for_ambiguous_duplicate_entry_updates(self):
        ''' Must throw Exception when attempts to update memo field for duplicate row
        '''
        pass


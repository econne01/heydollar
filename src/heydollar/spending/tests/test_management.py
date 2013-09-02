import os, datetime
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

    def test_can_parse_upload_file_date_column_to_date_object(self):
        ''' Must be able to convert a date string in upload file to date object
        '''
        upload_data = self.prepare_default_upload_file_data()
        # Test parsing of format YYYY-MM-DD
        upload_data[MintFileUploader.file_fields.date] = '2013-04-30'
        db_data = self.uploader.map_row_to_db_format(upload_data)
        date = datetime.date(2013, 4, 30)
        self.assertEqual(db_data[self.uploader.file_map[self.uploader.file_fields.date]], date)

    def test_can_parse_upload_file_description_field_with_tabs_to_string(self):
        ''' Must be able to convert a string object in upload file to string, even
            if it contains a '\t' or other delimiter character
        '''
        #@todo
        pass

    def test_can_parse_upload_file_amount_field_to_decimal(self):
        ''' Must be able to convert an amount string to decimal
        '''
        pass

    def test_can_parse_upload_file_category_field_to_new_category_object(self):
        ''' Must be able to convert category string to a new Category data object
            if none exists
        '''
        pass

    def test_can_parse_upload_file_category_field_to_existing_category_object(self):
        ''' Must be able to convert category string to an existing Category data object
            if it exists
        '''
        pass

    def test_throw_error_for_upload_file_account_field_of_new_account_object(self):
        ''' Must throw Exception for an account string of an Account object that does not exist
        '''
        pass

    def test_can_parse_upload_file_account_field_to_existing_account_object(self):
        ''' Must be able to convert account string to an existing Account data object
            if it exists
        '''
        pass

    def test_can_insert_new_upload_file_row_to_database(self):
        ''' Must insert record to database when uploading new transaction data
        '''
        pass

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


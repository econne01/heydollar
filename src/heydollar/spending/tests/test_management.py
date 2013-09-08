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
        self.account = AutoFixture(account_models.Account, generate_fk=True).create_one()
        
        self.account_map = account_models.AccountNameMap(
            name='Account Map Name',
            user=person,
            account=self.account
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

    def write_example_upload_file(self, filename, upload_data, repeat_rows=1):
        # Write the test data to a file
        ofile = open(filename, 'w')
        ofile.write('\t'.join(upload_data.keys()) + '\n')
        for i in range(repeat_rows):
            ofile.write('\t'.join([upload_data[k] for k in upload_data.keys()]) + '\n')
        ofile.close()

    def get_default_create_txn_data(self):
        ''' Setup a dictionary of default values for required fields to create a Transaction object
        '''
        upload_data = self.prepare_default_upload_file_data()
        date = datetime.datetime.strptime(upload_data[self.uploader.file_fields.date], '%m/%d/%Y')
        date = date.strftime('%Y-%m-%d')
        return {
            'post_date': date,
            'amount': upload_data[self.uploader.file_fields.amount],
            'account': self.account,
            'type': self.txn_type,
            'category': self.category,
            'description': upload_data[self.uploader.file_fields.description],
            'orig_description': upload_data[self.uploader.file_fields.original_description],
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
        self.write_example_upload_file(filename, upload_data)
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
        self.write_example_upload_file(filename, upload_data)
        # Upload the test data to database
        txn_cnt = spending_models.Transaction.objects.count()
        self.uploader.upload(filename)
        self.assertEqual(spending_models.Transaction.objects.count(), txn_cnt+1)

    def test_can_update_existing_upload_file_row_to_database(self):
        ''' Must update record in database when uploading existing transaction data
        '''
        upload_data = self.prepare_default_upload_file_data()
        new_notes = 'New notes to be saved'
        upload_data[self.uploader.file_fields.notes]=new_notes
        # Write the test data to a file
        filename = os.path.abspath(os.path.sep.join([settings.PROJECT_PATH, self.fake_filename]))
        self.write_example_upload_file(filename, upload_data)
        # Create an Entry in database with test data
        txn_data = self.get_default_create_txn_data()
        txn = spending_models.Transaction(**txn_data)
        txn.notes = 'Old notes to be edited'
        txn.save()
        # Upload the test data to database
        txn_cnt = spending_models.Transaction.objects.count()
        self.uploader.upload(filename)
        txn = spending_models.Transaction.objects.get(pk=txn.pk)
        self.assertEqual(spending_models.Transaction.objects.count(), txn_cnt)
        self.assertEqual(txn.notes, new_notes)

    def test_must_insert_duplicate_upload_file_row_to_database(self):
        ''' Must insert new record to database when uploading duplicate transaction data
            (ie, the same unique record fields occur multiple times in one upload file)
        '''
        upload_data = self.prepare_default_upload_file_data()
        # Write the test data to a file
        duplicate_cnt = 2
        filename = os.path.abspath(os.path.sep.join([settings.PROJECT_PATH, self.fake_filename]))
        self.write_example_upload_file(filename, upload_data, repeat_rows=duplicate_cnt)
        # Upload the test data to database
        txn_cnt = spending_models.Transaction.objects.count()
        self.uploader.upload(filename)
        self.assertEqual(spending_models.Transaction.objects.count(), txn_cnt+duplicate_cnt)

    def test_can_differentiate_duplicate_database_entries_by_notes_field(self):
        ''' Must select proper database entry to update (as needed) by matching notes field
        '''
        upload_data = self.prepare_default_upload_file_data()
        txn_cnt = spending_models.Transaction.objects.count()
        # Create 2 duplicate Transactions
        txn_data = self.get_default_create_txn_data()
        txn_data['notes'] = 'First Txn Notes'
        txn1 = spending_models.Transaction(**txn_data)
        txn1.save()
        notes2 = 'Second Txn Notes'
        txn_data['notes'] = notes2
        txn2 = spending_models.Transaction(**txn_data)
        txn2.save()
        self.assertEqual(spending_models.Transaction.objects.count(), txn_cnt+2)
        # Write data to a test file, with EDITED category for Txn2
        upload_data[self.uploader.file_fields.notes] = notes2
        category2 = AutoFixture(spending_models.Category).create_one()
        upload_data[self.uploader.file_fields.category] = category2.name
        filename = os.path.abspath(os.path.sep.join([settings.PROJECT_PATH, self.fake_filename]))
        self.write_example_upload_file(filename, upload_data)
        # Upload the test data to database. Should find and revise Txn2
        txn_cnt = spending_models.Transaction.objects.count()
        self.uploader.upload(filename)
        self.assertEqual(spending_models.Transaction.objects.count(), txn_cnt)
        txn2 = spending_models.Transaction.objects.get(pk=txn2.pk)
        print upload_data
        print self.category
        print category2
        self.assertEqual(txn2.category, category2)

    def test_throw_error_for_ambiguous_duplicate_entry_updates(self):
        ''' Must throw Exception when attempts to update memo field for duplicate row
        '''
        upload_data = self.prepare_default_upload_file_data()
        txn_cnt = spending_models.Transaction.objects.count()
        # Create 2 duplicate Transactions
        txn_data = self.get_default_create_txn_data()
        txn_data['notes'] = 'First Txn Notes'
        txn1 = spending_models.Transaction(**txn_data)
        txn1.save()
        notes2 = 'Second Txn Notes'
        txn_data['notes'] = notes2
        txn2 = spending_models.Transaction(**txn_data)
        txn2.save()
        self.assertEqual(spending_models.Transaction.objects.count(), txn_cnt+2)
        # Write data to a test file, with THIRD notes field
        notes3 = 'Third Txn Notes'
        upload_data[self.uploader.file_fields.notes] = notes3
        filename = os.path.abspath(os.path.sep.join([settings.PROJECT_PATH, self.fake_filename]))
        self.write_example_upload_file(filename, upload_data)
        # Upload should throw Error.  Impossible to know if Txn1 or Txn2 notes changed
        self.assertRaises(
            exceptions.HeydollarAmbiguousEntry,
            self.uploader.upload,
            filename
        )


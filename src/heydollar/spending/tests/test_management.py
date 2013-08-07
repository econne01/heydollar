from django.test import TestCase
from heydollar.spending.upload import MintFileUploader
from heydollar.spending.models import TransactionType, Category

class TestUploadMintHistoryTask(TestCase):
    ''' Test the upload Mint.com history (csv file) process
    '''

    def setUp(self):
        super(TestUploadMintHistoryTask, self).setUp()
        # Create necessary foreign key objects
        self.txn_type = TransactionType(name='debit')
        self.category = Category(name='Groceries')

        # Create a sample row of data from the default csv Mint history file download
        self.download_row_data = {
            'Date'                  : '01/01/2013',
            'Description'           : 'Some Description goes here',
            'Original Description'  : 'The Original Description -- often hard to read',
            'Amount'                : '123.45',
            'Transaction Type'      : self.txn_type.name,
            'Category'              : self.category.name,
            'Account Name'          : 'MyAccess Checking',
        }

    def test_can_map_download_file_row_data_to_database_spending_entry_object(self):
        ''' The map function should convert csv file format to a DB entry, with foreign key django objects
        '''
        uploader = MintFileUploader()
        db_data = uploader.map_row_to_db_format(self.download_row_data)
        # Test all fields properly converted to new data format and new labels
        self.assertEqual(db_data['type'], self.txn_type)
        self.assertEqual(db_data['category'], self.category)

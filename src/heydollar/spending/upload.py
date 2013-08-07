import csv
from heydollar.spending.models import Transaction, TransactionType, Category
from heydollar.account.models import AccountNameMap
from heydollar.utils.date import smart_parse_date

class MintHistoryFileSchema(object):
    ''' Simple class to define the column labels of a default Mint History csv file
    '''
    date = 'Date'
    description = 'Description'
    original_description = 'Original Description'
    account = 'Account Name'
    amount = 'Amount'
    category = 'Category'
    transaction_type = 'Transaction Type'
    notes = 'Notes'

class MintFileUploader():
    delimiter = '\t'
    # field_map converts file headers to database field names
    file_fields = MintHistoryFileSchema()
#    file_fields.date = 'Date'
#    file_fields.description = 'Description'
#    file_fields.original_description = 'Original Description'
#    file_fields.account = 'Account Name'
#    file_fields.amount = 'Amount'
#    file_fields.category = 'Category'
#    file_fields.transaction_type = 'Transaction Type'
#    file_fields.notes = 'Notes'
    
    field_map = {
        file_fields.date: 'post_date',
        file_fields.description: 'description',
        file_fields.original_description: 'orig_description',
        file_fields.amount: 'amount',
        file_fields.transaction_type: 'type',
        file_fields.category: 'category',
        file_fields.account: 'account',
        file_fields.notes: 'notes'
    }
    # User_id of account owner whose file is being uploaded
    user = 1 
    
    def insert_update(self, txn_data):
        ''' Parse the given data and either insert to database or update existing record
            @param dictionary txn_data. Row element data of a transaction
        '''
        transactions = Transaction.objects.filter(
            post_date = txn_data['post_date'],
            account = txn_data['account'],
            orig_description = txn_data['orig_description']
        )
        if transactions.count() == 0:
            print 'Adding transaction...'
            txn = Transaction()
            for field in txn_data:
                setattr(txn, field, txn_data[field])
            txn.save()
            print txn
        elif transactions.count() == 1:
            print 'Updating transaction...'
            for txn in transactions:
                for field in txn_data:
                    setattr(txn, field, txn_data[field])
                txn.save()
                print txn
        
    def map_row_to_db_format(self, row):
        ''' Create a new dictionary with same data, but converts file headers to database field names
            and finds Foreign Key objects from database, as needed
        '''
        db_row = {}
        # parse date
        if self.file_fields.date in row:
            field = self.file_fields.date
            db_row[self.field_map[field]] = smart_parse_date(row[field])
            del row[field]
            
        # parse account
        if self.file_fields.account in row:
            field = self.file_fields.account
            account_map = AccountNameMap.objects.get(
                user = self.user,
                name = row[field]
            )
            db_row[self.field_map[field]] = account_map.account
            del row[field]
            
        # parse transaction type
        if self.file_fields.transaction_type in row:
            field = self.file_fields.transaction_type 
            txn_type = TransactionType.objects.get(
                name = row[field]
            )
            db_row[self.field_map[field]] = txn_type
            del row[field]
                
        # parse category
        if self.file_fields.category in row:
            field = self.file_fields.category 
            category = Category.objects.get(
                name = row[field]
            )
            db_row[self.field_map[field]] = category
            del row[field]
            
        # parse amount
        if self.file_fields.amount in row:
            field = self.file_fields.amount
            db_row[self.field_map[field]] = float(row[field])
            del row[field]
        
        for field in row:
            if field in self.field_map:
                db_row[self.field_map[field]] = row[field]
        return db_row
    
    def upload(self, filename):
        ''' Parse the given filename and insert/update the database with the financial transaction history
        '''
        ifile = open(filename, 'r')
        reader = csv.DictReader(ifile, delimiter=self.delimiter)
        for row in reader:
            txn_data = self.map_row_to_db_format(row)
            self.insert_update(txn_data)
        
if __name__ == '__main__':
    filename = r'C:\Users\Eric\Documents\Finances\Mint Project\transactions_testing.txt'
    loader = MintFileUploader()
    loader.upload(filename)
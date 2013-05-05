import csv
from datetime import datetime
from heydollar.spending.models import Transaction
from heydollar.account.models import AccountNameMap

def smart_parse_date(datestring, in_format=None, out_format='%Y-%m-%d'):
    ''' Convert the datestring to YYYY-MM-DD format
        @param string datestring
        @param string in_format. Format of input string, optional
        @param string out_format. Format to set return string
    '''
    if in_format is None:
        in_format = '%m/%d/%Y'
    d = datetime.strptime(datestring, in_format)
    return d.strftime(out_format)
    

class MintFileUploader():
    delimiter = '\t'
    # field_map converts file headers to database field names
    field_map = {
        'Date': 'post_date',
        'Description': 'description',
        'Original Description': 'orig_description',
        'Amount': 'amount',
        'Transaction Type': 'txn_type',
        'Category': 'category',
        'Account Name': 'account',
        'Notes': 'notes'
    }
    # User_id of account owner whose file is being uploaded
    user = 1 
    
    def map_row(self, row):
        ''' Create a new dictionary with same data, but converts file headers to database field names
        '''
        db_row = {}
        # parse date
        if 'Date' in row:
            field = 'Date'
            db_row[self.field_map[field]] = smart_parse_date(row[field])
            del row[field]
            
        # parse account
        if 'Account Name' in row:
            field = 'Account Name'
            account = AccountNameMap.objects.get(
                user = self.user,
                name = row[field]
            )
            db_row[self.field_map[field]] = account
            del row[field]
                
        for field in row:
            if field in self.field_map:
                db_row[self.field_map[field]] = row[field]
            else:
                db_row[field] = row[field]
        return db_row
    
    def upload(self, filename):
        ''' Parse the given filename and insert/update the database with the financial transaction history
        '''
        ifile = open(filename, 'r')
        reader = csv.DictReader(ifile, delimiter=self.delimiter)
        for row in reader:
            txn_data = self.map_row(row)
            print txn_data
            exit()
            Transaction.insert_update(txn_data)
            exit()
        
if __name__ == '__main__':
    filename = r'C:\Users\Eric\Documents\Finances\Mint Project\transactions_testing.txt'
    loader = MintFileUploader()
    loader.upload(filename)
import csv, os

from django.http import HttpResponseRedirect

from heydollar import exceptions
from heydollar.spending.models import Transaction, Category
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
    delim_choices = [
        ',',
        '/t',
    ]
    # field_map converts file headers to database field names
    file_fields = MintHistoryFileSchema()

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
    #@todo: make this arbitrary
    user = 1

    def __init__(self, *args, **kwargs):
        self.processed_txns = []

    def insert_update(self, txn_data):
        ''' Parse the given data and either insert to database or update existing record
            @param dictionary txn_data. Row element data of a transaction
        '''
        transactions = Transaction.objects.filter(
            post_date = txn_data['post_date'],
            account = txn_data['account'],
            orig_description = txn_data['orig_description'],
            amount = txn_data['amount']
        )
        txn = None
        if transactions.count() == 0:
            # Add transaction
            txn = Transaction()
        elif transactions.count() == 1:
            # Check if this is a duplicate record already processed in this file
            # If so, create new, separate duplicate record
            if transactions[0] in self.processed_txns:
                txn = Transaction()
            else:
                # Update transaction
                txn = transactions[0]
        elif transactions.count() > 1:
            # Found duplicate entries
            # Try to select a single entry from Notes field
            notes_txns = transactions.filter(notes=txn_data['notes'])
            if notes_txns.count() == 1:
                txn = notes_txns[0]
        if txn is None:
            raise exceptions.HeydollarAmbiguousEntry(
                'Could not determine which entry data refers to',
                txn_data
            )
        for field in txn_data:
            setattr(txn, field, txn_data[field])
        txn.save()
        # Track each processed transaction in case its duplicate is
        # later processed
        if txn not in self.processed_txns:
            self.processed_txns.append(txn)
        return txn

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
            account_filter = AccountNameMap.objects.filter(
                user = self.user,
                name = row[field]
            )
            if account_filter.count() < 1:
                raise exceptions.HeydollarDoesNotExist(
                    'This Account (%s), please create it then re-upload'
                    % (row[field]),
                    error_field = 'account_name',
                    error_value = row[field]
                )
            elif account_filter.count() == 1:
                db_row[self.field_map[field]] = account_filter[0].account
                del row[field]
            else:
                raise Exception('There are multiple Accounts specified for name %s' %row[field])

        # parse transaction type
        if self.file_fields.transaction_type in row:
            field = self.file_fields.transaction_type
            db_row[self.field_map[field]] = row[field]
            del row[field]

        # parse category
        if self.file_fields.category in row:
            field = self.file_fields.category
            category = Category.objects.get_or_create(
                name = row[field]
            )[0]
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

    def get_delimiter(self, file):
        ''' Open the file to determine the most likely delimiter choice to parse with
        '''
        headers = file.readline()

        max_delim = ''
        max_cnt = 0
        for delim in self.delim_choices:
            cnt = headers.count(delim)
            if cnt > max_cnt:
                max_cnt = cnt
                max_delim = delim
        return max_delim

    def upload(self, file):
        ''' Parse the given filename and insert/update the database with the financial transaction history
        '''
        try:
            delim = self.get_delimiter(file)
            reader = csv.DictReader(file, delimiter=delim)
        except Exception:
            raise exceptions.HeydollarInvalidUploadFile('The file you are trying to upload has an error')
        is_first_row = True
        for row in reader:
            if is_first_row:
                if not set(self.field_map.keys()).issubset(set(row.keys())):
                    raise exceptions.HeydollarInvalidUploadFile('Please upload a file with expected column headers of %s, not %s'
                        % (','.join(self.field_map.keys()), ','.join(row.keys())))
                is_first_row = False
                continue

            txn_data = self.map_row_to_db_format(row)
            self.insert_update(txn_data)

import csv
from heydollar.spending.models import Transaction, TransactionType, Category
from heydollar.account.models import AccountNameMap

def upload_mint_transaction_history_csv_file(history_file):
    ''' Upload a CSV file with Mint.com transaction history entries into database,
        inserting rows for new records and updating existing records as needed
    '''
    return
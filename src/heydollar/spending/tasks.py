import csv
from datetime import datetime
from decimal import Decimal
from heydollar.spending.models import Transaction, TransactionType, Category
from heydollar.account.models import AccountNameMap

def upload_mint_transaction_history_csv_file(history_file, delim='","'):
    ''' Upload a CSV file with Mint.com transaction history entries into database,
        inserting rows for new records and updating existing records as needed
        File format = (PostDate, Description, OrigDescription, Amount, Txn Type, Category, Account, Labels, Notes)
    '''
    headers = history_file.readline().strip().split(delim)
    headers = [elem.replace('"', '') for elem in headers]
    for row in history_file.readlines():
        row_elems = row.strip().split(delim)
        row_elems = [elem.replace('"', '') for elem in row_elems]
        post_date   = row_elems[0]
        description = row_elems[1]
        orig_desc   = row_elems[2]
        amount      = row_elems[3]
        txn_type    = row_elems[4]
        category    = row_elems[5]
        account     = row_elems[6]
        labels      = row_elems[7]
        notes       = row_elems[8]

        # Convert post_date to Date object
        post_date = datetime.strptime(post_date, '%m/%d/%Y').date()
        # Convert amount to Decimal
        amount = Decimal(amount)
        # Convert txn_type to a TransactionType object
        txn_type = TransactionType.objects.get(name=txn_type)
        # Convert category to a Category object
        category = Category.objects.get_or_create(name=category)[0]
        # Convert account name to an Account object
        account = AccountNameMap.objects.get(name=account).account
        
        # Try to find any transactions that match the OrigDesc, Date and Amount
        txns = Transaction.objects.filter(
            orig_description = orig_desc,
            post_date = post_date,
            amount = amount
        )
        if txns.count() == 0:
            # If no entry, create one
            txn = Transaction(
                post_date = post_date,
                description = description,
                orig_description = orig_desc,
                amount = amount,
                category = category,
                type = txn_type,
                account = account,
                notes = notes
            )
            txn.save()
        elif txns.count() == 1:
            txn = txns[0]
            txn.post_date = post_date
            txn.description = description
            txn.orig_description = orig_desc
            txn.amount = amount
            txn.category = category
            txn.type = txn_type
            txn.account = account
            txn.notes = notes
            txn.save()
    return
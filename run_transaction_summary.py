import click
import csv
from decimal import Decimal

from config.account_owner import ACCOUNT_OWNER_MAP
from config.category_map import SUMMARY_CATEGORIES, \
        BROAD_TO_SUMMARY_CATEGORY_MAP, \
        DETAIL_TO_SEMI_BROAD_CATEGORY_MAP


def get_summary_spending_category(txn_category):
    """Return the SUMMARY (least detailed) category that includes the given transaction category"""
    if txn_category in DETAIL_TO_SEMI_BROAD_CATEGORY_MAP:
        mid_category = DETAIL_TO_SEMI_BROAD_CATEGORY_MAP[txn_category]
        return BROAD_TO_SUMMARY_CATEGORY_MAP[mid_category]
    elif txn_category in BROAD_TO_SUMMARY_CATEGORY_MAP:
        return BROAD_TO_SUMMARY_CATEGORY_MAP[mid_category]
    else:
        print(txn_category, ' does not map to a SUMMARY category!')
        return txn_category

@click.command()
@click.argument('transaction_file_path', type=click.Path(exists=True))
def cli(transaction_file_path):
    """CLI script to aggregate Mint.com transaction data"""
    click.echo('Hello World!')

    SPENDING_SUMMARY = { c: Decimal('0.0') for c in SUMMARY_CATEGORIES }

    row_count = 0
    with open(transaction_file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        HEADERS = next(csvreader)
        for row in csvreader:
            row_count += 1
            if row_count > 10:
                break
            # Each entry in the CSV is a "string" enclosed in quotes, so let's remove the quotes
            row_dict = {HEADERS[i][1:-1]: row[i][1:-1] for i in range(len(HEADERS))}
            row_dict['Amount'] = Decimal(row_dict['Amount'])
            if row_dict['Account Name'] not in ACCOUNT_OWNER_MAP:
                print('Account Owner not found for: ', row_dict['Account Name'])
                continue
            elif ACCOUNT_OWNER_MAP[row_dict['Account Name']] != 'Eric & Gopi':
                print('Account was for someone else!', row_dict['Account Name'])
                continue

            if row_dict['Transaction Type'] == 'debit':
                row_dict['Amount'] *= -1

            category = get_summary_spending_category(row_dict['Category'])

            SPENDING_SUMMARY[category] += row_dict['Amount']

    print(SPENDING_SUMMARY)

import click
import csv
from datetime import date, datetime
from decimal import Decimal

from config.account_owner import ACCOUNT_OWNER_MAP
from config.category_map import SUMMARY_CATEGORIES, \
        CATEGORIES_TO_IGNORE, \
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


def standardize_date_format(txn_date):
    """Convert a date string formatted as MM/DD/YYYY to YYYY-MM-DD"""
    if '/' in txn_date:
        mm, dd, yyyy = txn_date.split('/')
        return date(int(yyyy), int(mm), int(dd)).strftime('%Y-%m-%d')
    return txn_date


@click.command()
@click.argument('transaction_file_path', type=click.Path(exists=True))
@click.option('--start-date',
              default='2001-01-01',
              help='The start date of the range of transactions you want to report on.')
@click.option('--end-date',
              default=None,
              help='The end date of the range of transactions you want to report on. '
                  'Default is up to current date')
@click.option('--time-interval',
              type=click.Choice(['D', 'W', 'M', 'Y'], case_sensitive=False),
              help='The time interval for which you want to group spending in your report. '
                  'It could be by day, week, month or year')
def cli(transaction_file_path, start_date, end_date, time_interval):
    """CLI script to aggregate Mint.com transaction data"""
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    SPENDING_SUMMARY = { c: Decimal('0.0') for c in SUMMARY_CATEGORIES }

    row_count = 0
    with open(transaction_file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', doublequote=False, quotechar='"')
        HEADERS = next(csvreader)
        for i, row in enumerate(csvreader):
            row_count += 1
            # Each entry in the CSV is a "string" enclosed in quotes, so let's remove the quotes
            row_dict = {HEADERS[i]: row[i] for i in range(len(HEADERS))}

            # Do some validation that this row meets criteria for our report
            # CHECK 1: Is txn for the right ACCOUNT OWNER?
            if row_dict['Account Name'] not in ACCOUNT_OWNER_MAP:
                print('Account Owner not found for: ', row_dict['Account Name'])
                print(row)
                raise Exception('Account Owner not found')
                continue
            elif ACCOUNT_OWNER_MAP[row_dict['Account Name']] != 'Eric & Gopi':
                print('Account was for someone else!', row_dict['Account Name'])
                continue
            # CHECK 2: Is txn in the right DATE range?
            txn_date = standardize_date_format(row_dict['Date'])
            if txn_date < start_date or txn_date > end_date:
                continue

            # If row qualifies, then add it to the appropriate bucket of SPENDING_SUMMARY
            row_dict['Amount'] = Decimal(row_dict['Amount'])
            if row_dict['Transaction Type'] == 'debit':
                row_dict['Amount'] *= -1

            category = get_summary_spending_category(row_dict['Category'])
            if category in CATEGORIES_TO_IGNORE:
                continue

            SPENDING_SUMMARY[category] += row_dict['Amount']

    print(SPENDING_SUMMARY)

import click
import csv
from datetime import date, datetime
from decimal import Decimal

from config.account_owner import ACCOUNT_OWNER_MAP
from config.category_map import SUMMARY_CATEGORIES, \
        CATEGORIES_TO_IGNORE, \
        BROAD_TO_SUMMARY_CATEGORY_MAP, \
        DETAIL_TO_SEMI_BROAD_CATEGORY_MAP, \
        SUMMARY_CATEGORIES


class DataCleanlinessException(Exception):
    """An error in the input data -- something is unknown and cannot be properly handled"""
    pass


def get_summary_spending_category(txn_category):
    """Return the SUMMARY (least detailed) category that includes the given transaction category"""
    if txn_category in DETAIL_TO_SEMI_BROAD_CATEGORY_MAP:
        mid_category = DETAIL_TO_SEMI_BROAD_CATEGORY_MAP[txn_category]
        return BROAD_TO_SUMMARY_CATEGORY_MAP[mid_category]
    elif txn_category in BROAD_TO_SUMMARY_CATEGORY_MAP:
        return BROAD_TO_SUMMARY_CATEGORY_MAP[mid_category]
    elif txn_category in SUMMARY_CATEGORIES:
        return txn_category
    else:
        raise DataCleanlinessException(f'{txn_category} does not map to a SUMMARY category!')


def date_to_interval_date(txn_date, time_interval):
    """
    Convert a date to a "start of" date for a time interval
    depending on what time of time_interval is given.
    @param {String} txn_date: eg, 2020-12-31
    @param {String} time_interval: one of [D, W, M, Y]
    @return {String} eg, '2020-12-01'
    """
    if time_interval == 'Y':
        return f'{txn_date[:4]}-01-01'
    elif time_interval in ('M', 'W'):
        return f'{txn_date[:7]}-01'
    else:
        return txn_date


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
@click.option('--owner',
              default='Eric & Gopi',
              help='Which account owner do you want to summarize spending for?')
@click.option('--run-mode',
              default='summary',
              type=click.Choice(['summary', 'end-on-error', 'data-scrub'], case_sensitive=False),
              help='The mode to run this script, whether to make best guess in summary (summary), '
                  'run until any data issue (end-on-error), or find all data issues (data-scrub)')
def cli(transaction_file_path, start_date, end_date, time_interval, owner, run_mode):
    """CLI script to aggregate Mint.com transaction data"""
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    SPENDING_SUMMARY = {}
    DATA_SCRUB_ISSUES = {
        'UNKNOWN Accounts (Missing Owner)': {},
        'UNKNOWN Transaction Categories (Missing in Map)': {},
    }

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
                if run_mode == 'end-on-error':
                    print('Account Owner not found for: ', row_dict['Account Name'])
                    print(row)
                    raise Exception('Account Owner not found')
                else:
                    DATA_SCRUB_ISSUES['UNKNOWN Accounts (Missing Owner)'][row_dict['Account Name']] = row_dict['Account Name']
                continue
            elif ACCOUNT_OWNER_MAP[row_dict['Account Name']] != owner:
                if run_mode == 'data-scrub':
                    print('Account was for someone else!', row_dict['Account Name'])
                continue
            # CHECK 2: Is txn in the right DATE range?
            txn_date = standardize_date_format(row_dict['Date'])
            if txn_date < start_date or txn_date > end_date:
                continue
            summary_date = date_to_interval_date(txn_date, time_interval)
            if summary_date not in SPENDING_SUMMARY:
                SPENDING_SUMMARY[summary_date] = { c: Decimal('0.0') for c in SUMMARY_CATEGORIES }

            # If row qualifies, then add it to the appropriate bucket of SPENDING_SUMMARY
            row_dict['Amount'] = Decimal(row_dict['Amount'])
            if row_dict['Transaction Type'] == 'debit':
                row_dict['Amount'] *= -1

            try:
                category = get_summary_spending_category(row_dict['Category'])
            except DataCleanlinessException as e:
                if run_mode == 'end-on-error':
                    raise e
                else:
                    DATA_SCRUB_ISSUES['UNKNOWN Transaction Categories (Missing in Map)'][row_dict['Category']] = row_dict['Category']
                    category = 'Other'

            if category in CATEGORIES_TO_IGNORE:
                continue

            SPENDING_SUMMARY[summary_date][category] += row_dict['Amount']

    if run_mode == 'data-scrub':
        print(DATA_SCRUB_ISSUES)
    else:
        print('Data Scrubbing Issues discovered:')
        print(DATA_SCRUB_ISSUES)
        print('\n')
        print('Spending Summary:')
        interval_dates = list(SPENDING_SUMMARY.keys())
        interval_dates.sort()
        with open('summary.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(['Interval Date'] + SUMMARY_CATEGORIES)
            for idate in interval_dates:
                print(idate)
                print(SPENDING_SUMMARY[idate])
                csvwriter.writerow([idate] + [SPENDING_SUMMARY[idate][category] for category in SUMMARY_CATEGORIES])

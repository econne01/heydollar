# heydollar

Personal finance management tool that extends mint.com functionality

This project contains a script for Eric's personal use to aggregate transaction data from Mint.com
into annual spending totals

contact:
eric.connelly08@gmail.com

## Setup
_Optional_
```
mkvirtualenv -p `which python3` heydollar
workon heydollar
python setup.py develop
```

You will also need a Mint.com account. Login manually in a browser and download an export `csv` file of your
transaction history.

Copy the `config/account_owner_DO_NOT_MODIFY.py` file to `config/account_owner.py` locally and fill in the
account name and account owner of all existing (and historical) account names in your Mint.com transaction history.
This can be used to filter out transactions from accounts that belong to other members of your household (eg,
a college fund for children that should not count toward your own net worth or spending).

## Usage
This script is designed to take a detailed transaction history from Mint.com and output a summary of spending over time.
The default mode is to aggregate spending into broad categories (eg, "Housing" or "Food"), per *month*.

You can run the summary script in default mode, such as
```
run_transaction_summary /path/to/transactions.csv
```
Or you can choose a specifice date range and time-interval (Day, Week, Month or Year), such as
```
run_transaction_summary /path/to/transactions.csv --start-date 2020-01-01 --end-date 2020-03-31 --time-interval M
```

### Data Scrubbing and troubleshooting
You may notice that not all transactions are properly categorized, or that not all categories are known.
For example, say that at some point "Daycare Tuition" becomes a new category. The script will mark this as "Unknown"
spending. You can view a list of un-identified categories by running the script in "data-scrub" mode.

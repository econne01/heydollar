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

## Usage
```
run_transaction_summary.py /path/to/transactions.csv
```

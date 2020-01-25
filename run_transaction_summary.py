import click
import csv

from config.account_owner import ACCOUNT_OWNER_MAP

@click.command()
@click.argument('transaction_file_path', type=click.Path(exists=True))
def cli(transaction_file_path):
    """CLI script to aggregate Mint.com transaction data"""
    click.echo('Hello World!')

    row_count = 0
    with open(transaction_file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        HEADERS = next(csvreader)
        print(HEADERS)
        for row in csvreader:
            row_count += 1
            if row_count > 10:
                break
            print(', '.join(row))


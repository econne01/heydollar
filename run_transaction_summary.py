import click

@click.command()
@click.argument('transaction_file_path', type=click.File('r'))
def cli(transaction_file_path):
    """CLI script to aggregate Mint.com transaction data"""
    click.echo('Hello World!')

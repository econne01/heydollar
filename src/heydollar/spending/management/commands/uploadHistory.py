from django.core.management.base import BaseCommand, CommandError
from heydollar.spending import upload

class Command(BaseCommand):
    help = 'Uploads the given filename to database'

    def handle(self, *args, **options):
        filename = r'C:\Users\Eric\Documents\Finances\Mint Project\transactions_testing.txt'
        loader = upload.MintFileUploader()
        loader.upload(filename)
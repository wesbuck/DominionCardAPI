from django.core.management.base import BaseCommand
from cards.models import Card
import csv


class Command(BaseCommand):
    help = 'Ingests the specified CSV file into the Cards table'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file to be ingested')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        with open(csv_file, encoding="latin-1") as datafile:
            reader = csv.DictReader(datafile)
            for row in reader:
                card = Card()
                for field, data in row.items():
                    if '' != data:  # only ingest fields with data
                        setattr(card, field, data)
                card.save()

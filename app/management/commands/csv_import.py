from django.core.management.base import BaseCommand
from app.models.repository import Repository
import csv


class Command(BaseCommand):
    args = '<csv_file>'
    help = 'Imports a CSV file of Repositories'

    def handle(self, *args, **options):
        path = args[0]
        with open(path, 'rb') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in csvreader:
                print "importing %s" % row[0]
                Repository(
                    name=row[0], short_name=row[1],
                    source_type=row[2], source_url=row[3], remote_url=row[4]
                ).save()

import argparse
import csv

from django.core.management.base import BaseCommand

import docsearch.models


class Command(BaseCommand):
    help = 'Import document metadata from a source file'

    def add_arguments(self, parser):
        parser.add_argument(
            'infile',
            type=argparse.FileType('r'),
            help='The input file to import (must be a .csv file)'
        )
        parser.add_argument(
            'model',
            help='The class name of the model represented by this source file'
        )
        parser.add_argument(
            '--truncate',
            action='store_true',
            default=False,
            help='Truncate the table before performing the import'
        )

    def handle(self, *args, **options):
        Model = getattr(docsearch.models, options['model'])

        if options['truncate'] is True:
            Model.objects.all().delete()

        reader = csv.DictReader(options['infile'])

        header_to_model_fields = {field: field.replace(' ', '_')
                                  for field in reader.fieldnames}

        for row in reader:
            metadata = {header_to_model_fields[field]: value or None
                        for field, value in row.items()}

            s3_path = f'{Model.s3_prefix}/{metadata["source_file"]}'
            metadata['source_file'] = s3_path

            obj = Model(**metadata)
            obj.save()

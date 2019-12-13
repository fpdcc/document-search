import argparse
import csv

from django.core.management.base import BaseCommand
from django.db import connection, transaction

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

    @transaction.atomic
    def handle(self, *args, **options):
        Model = getattr(docsearch.models, options['model'])

        if options['truncate'] is True:
            with connection.cursor() as curs:
                curs.execute(
                    f'TRUNCATE {Model._meta.db_table} RESTART IDENTITY'
                )

        reader = csv.DictReader(options['infile'])

        # Fieldnames in the source CSV should be identical to model attributes,
        # except they have spaces instead of underscores
        header_to_model_fields = {field: field.replace(' ', '_')
                                  for field in reader.fieldnames}

        for row in reader:
            # Make sure to convert empty strings to NULL
            metadata = {header_to_model_fields[field]: value or None
                        for field, value in row.items()}
            # Document files are stored on S3, so we need to save a file string
            # corresponding to the appropriate S3 prefix for each document type
            s3_path = f'{Model.source_file.field.upload_to}/{metadata["source_file"]}'
            metadata['source_file'] = s3_path

            obj = Model(**metadata)
            obj.save()

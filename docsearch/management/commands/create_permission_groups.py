from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Permission, Group
from django.db.models import Q
from django.db import transaction


class Command(BaseCommand):
    help = 'Create the basic Groups for the docsearch app'

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            default=False
        )

    @transaction.atomic
    def handle(self, *args, **options):
        doc_permissions = Permission.objects.filter(
            content_type__app_label='docsearch'
        )

        read_permissions = doc_permissions.filter(codename__startswith='view_')
        if read_permissions.count() == 0:
            raise CommandError(
                'Failed to create Groups: No docsearch read permissions found'
            )

        write_permissions = read_permissions.union(doc_permissions.filter(
            Q(codename__startswith='add_') |
            Q(codename__startswith='change_') |
            Q(codename__startswith='delete_')
        ))
        if read_permissions.count() == 0:
            raise CommandError(
                'Failed to create Groups: No docsearch write permissions found'
            )

        read_only, _ = Group.objects.get_or_create(name='Read Only')
        read_only.permissions.set(read_permissions)
        read_only.save()

        read_write, _ = Group.objects.get_or_create(name='Read/Write')
        read_write.permissions.set(write_permissions)
        read_write.save()

        if options['verbose']:
            self.stdout.write(
                self.style.SUCCESS(
                    'Created {} and {} permission groups'.format(
                        read_only.name, read_write.name
                    )
                )
            )

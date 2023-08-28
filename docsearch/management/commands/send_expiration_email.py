from docsearch.models import License
from docsearch.settings import BASE_URL
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

import datetime
from csv import DictWriter
from io import StringIO


class Command(BaseCommand):
    help = (
        "Send notification emails for nearly expired licenses."
    )

    def generate_csv(self, licenses):
        file = StringIO()
        field_names = ["license_number", "end_date", "url"]
        header = ["License Number", "End Date", "Link"]
        writer = DictWriter(file, fieldnames=field_names)

        writer.writer.writerow(header)
        for l in licenses:
            writer.writerow(l)

        return file

    def handle(self, *args, **options):
        dates_to_exclude = ['continuous', 'indefinite', 'perpetual', 'cancelled', 'TBD']
        licenses = License.objects.exclude(end_date=None).exclude(end_date__in=dates_to_exclude)
        current_year = datetime.date.today().year

        near_expired = []
        for l in licenses:
            # The format is YYYY-MM-DD
            year, month, day = [int(time) for time in l.end_date.split("-")]

            end_date = datetime.date(year, month, day)
            if end_date.year == current_year:
                obj = {
                    "url": BASE_URL + l.get_absolute_url(),
                    "license_number": l.license_number,
                    "end_date": end_date
                }

                near_expired.append(obj)
        
        body = render_to_string(
            'emails/license_expiration.html',
            {
                'n_licenses': str(len(near_expired)),
                "year": str(current_year)
            },
        )
        
        email = EmailMessage(
            subject="Licenses expiring this year",
            body=body,
            to=["example@email.com"],  # TODO: get recipients from database
            from_email="example@email.com",  # TODO: assign a valid sender email
        )

        if len(near_expired) > 0:
            attachment = self.generate_csv(near_expired)
            email.attach('expiring_licenses_{}.csv'.format(str(current_year)), attachment.read())

        email.content_subtype = 'html'
        email.send()

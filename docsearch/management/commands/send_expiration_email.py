from docsearch.models import License, NotificationSubscription
from docsearch.settings import BASE_URL
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

import datetime
from dateutil.relativedelta import relativedelta
from csv import DictWriter
from io import StringIO


class Command(BaseCommand):
    help = (
        "Send notification emails for nearly expired licenses."
    )

    def generate_csv(self, licenses):
        '''
        Create a file in memory with details of licenses, intended to be written later
        '''
        file = StringIO()
        field_names = ["license_number", "end_date", "url"]
        header = ["License Number", "End Date", "Link"]
        writer = DictWriter(file, fieldnames=field_names)

        writer.writer.writerow(header)
        for l in licenses:
            writer.writerow(l)

        return file
    
    def get_near_expired_licenses(self, present, future_limit):
        '''
        Returns all licenses expiring between now and a future date
        '''
        dates_to_exclude = ['continuous', 'indefinite', 'perpetual', 'cancelled', 'TBD']
        licenses = License.objects.exclude(end_date=None).exclude(end_date__in=dates_to_exclude)

        result = []
        for l in licenses:
            # The format is YYYY-MM-DD
            year, month, day = [int(time) for time in l.end_date.split("-")]

            end_date = datetime.date(year, month, day)
            if present <= end_date and end_date <= future_limit:
                obj = {
                    "url": BASE_URL + l.get_absolute_url(),
                    "license_number": l.license_number,
                    "end_date": end_date
                }

                result.append(obj)

        return result

    def handle(self, *args, **options):
        today = datetime.date.today()

        if NotificationSubscription.objects.filter(notification_date=today).exists():
            self.stdout.write("Checking for licenses expiring soon...")

            one_year_from_now = datetime.date.today() + relativedelta(years=1)
            near_expired = self.get_near_expired_licenses(today, one_year_from_now)
            subscribers = NotificationSubscription.objects.filter(notification_date=today)

            # Prepare email
            recipients = []
            for sub in subscribers:
                recipients.append(sub.user.email)

            body = render_to_string(
                'emails/license_expiration.html',
                {
                    "n_licenses": str(len(near_expired)),
                    "date_range_start": today.strftime("%m/%d/%Y"),
                    "date_range_end": one_year_from_now.strftime("%m/%d/%Y"),
                },
            )

            email = EmailMessage(
                subject="Licenses expiring in the next 12 months",
                body=body,
                to=recipients,
            )

            self.stdout.write(f"{len(near_expired)} license(s) found")
            if len(near_expired) > 0:
                attachment = self.generate_csv(near_expired)
                email.attach('expiring_licenses_{}.csv'.format(str(today.year)), attachment.getvalue())

            self.stdout.write("Sending emails...")
            email.content_subtype = 'html'
            email.send()
            self.stdout.write(self.style.SUCCESS("Emails sent!"))

            # Update each users' notification date after sending emails
            for sub in subscribers:
                sub.notification_date = one_year_from_now
                sub.save()

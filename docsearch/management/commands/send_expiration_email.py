from docsearch.models import License, NotificationSubscription
from docsearch.settings import BASE_URL
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.db import transaction

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
    
    def attach_csv(self, email, near_expired, date):
        '''
        If any expiring licenses exist, attach a csv report to the email
        '''
        if len(near_expired) > 0:
            attachment = self.generate_csv(near_expired)
            email.attach('expiring_licenses_{}.csv'.format(str(date.year)), attachment.getvalue())
    
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
    
    def prep_email(self, subscribers, near_expired, date_range_start, date_range_end, subject):
        '''
        Assign recipients and build the contents of the email
        '''
        recipients = []
        for sub in subscribers:
            recipients.append(sub.user.email)
            sub.notification_date = date_range_end
            sub.save()

        body = render_to_string(
            'emails/license_expiration.html',
            {
                "n_licenses": str(len(near_expired)),
                "date_range_start": date_range_start.strftime("%m/%d/%Y"),
                "date_range_end": date_range_end.strftime("%m/%d/%Y"),
            },
        )

        email = EmailMessage(
            subject=subject,
            body=body,
            to=recipients,
        )
        email.content_subtype = 'html'

        self.attach_csv(email, near_expired, date_range_start)

        return email

    @transaction.atomic
    def handle(self, *args, **options):
        today = datetime.date.today()

        if NotificationSubscription.objects.filter(notification_date=today).exists():
            self.stdout.write("Checking for licenses expiring soon...")

            one_year_from_now = datetime.date.today() + relativedelta(years=1)
            near_expired = self.get_near_expired_licenses(today, one_year_from_now)
            self.stdout.write(f"{len(near_expired)} license(s) found")

            subscribers = NotificationSubscription.objects.filter(notification_date=today)
            subject = "Licenses expiring in the next 12 months"
            email = self.prep_email(
                subscribers=subscribers,
                near_expired=near_expired,
                date_range_start=today,
                date_range_end=one_year_from_now,
                subject=subject
            )

            self.stdout.write("Sending emails...")
            email.send()
            self.stdout.write(self.style.SUCCESS("Emails sent!"))                

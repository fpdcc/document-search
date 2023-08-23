from ...models import License
from ...settings import BASE_URL
from django.core.management.base import BaseCommand

import datetime
from dateutil.relativedelta import relativedelta


class Command(BaseCommand):
    help = (
        "Send notification emails for nearly expired licenses."
    )

    def handle(self, *args, **options):
        dates_to_exclude = ['continuous', 'indefinite', 'perpetual', 'cancelled', 'TBD']
        licenses = License.objects.exclude(end_date=None).exclude(end_date__in=dates_to_exclude)
        six_months_from_now = datetime.date.today() + relativedelta(months=6)

        near_expired = []
        for l in licenses:
            # The format is YYYY-MM-DD
            year, month, day = [int(time) for time in l.end_date.split("-")]

            end_date = datetime.date(year, month, day)
            if datetime.date.today() <= end_date and end_date <= six_months_from_now:
                obj = {
                    "url": BASE_URL + l.get_absolute_url(),
                    "license_number": l.license_number,
                }

                near_expired.append(obj)

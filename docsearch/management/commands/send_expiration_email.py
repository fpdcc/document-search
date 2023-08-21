from ...models import License
import datetime

# This command should run every day, get all the licenses,
# check their end_date's, and get all the ones who's expiration date is coming up in the next 6 months or something
# maybe make it a csv? or to start we can just put the urls in there. it seems to be in the format of
# <domain>/licenses/<id>

def get_near_expired_licenses():
    dates_to_exclude = ['continuous', 'indefinite', 'perpetual', 'cancelled', 'TBD']
    licenses = License.objects.exclude(end_date=None).exclude(end_date__in=dates_to_exclude)
    near_expired = []
    for l in licenses:
        today = datetime.datetime.now()
        # The format is YYYY-MM-DD
        year = l.end_date.split("-")[0]
        month = l.end_date.split("-")[1]
        day = l.end_date.split("-")[2]
        print(l.end_date)
        print(l.get_absolute_url())
        print('---------')
        # TODO: set a settings var that contains the domain name and concat that to the url
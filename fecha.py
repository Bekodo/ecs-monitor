#!/opt/local/bin/python2.7

from datetime import datetime, timedelta
from pytz import timezone
from pprint import pprint
# import datetime
# import pytz

fmt = "%Y-%m-%d %H:%M:%S %Z%z"

# source_date = datetime.datetime.now()
# source_time_zone = pytz.timezone('Europe/Amsterdam')
# source_date_with_timezone = source_time_zone.localize(source_date)
# target_time_zone = pytz.timezone('Europe/Dublin')
# target_date_with_timezone = source_date_with_timezone.astimezone(target_time_zone)
# print target_date_with_timezone

now_utc = datetime.now()
amsterdam_tz = timezone('Europe/Amsterdam')
now_tz = amsterdam_tz.localize(now_utc)

dublin_tz = timezone('Europe/Dublin')
date_tz_dublin = now_tz.astimezone(dublin_tz)
# dublin_tz = timezone('Europe/Dublin')
# now_tz = dublin_tz.localize(now_utc)
date_tz_dublin = now_tz.astimezone(dublin_tz)


print date_tz_dublin.strftime(fmt)


# Current time in UTC
# now_utc = datetime.now()
# now_dublin = now_utc.astimezone(timezone('Europe/Dublin'))
# StartTime = now_dublin - timedelta(minutes=5)
# EndTime = now_dublin - timedelta(minutes=0)
# print('Temps StartTime\t{}'.format(StartTime.strftime(fmt)))
# print('Temps EndTime\t{}'.format(EndTime.strftime(fmt)))




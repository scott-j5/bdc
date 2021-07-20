import datetime

from django.utils.timezone import make_aware


def parse_date_range(range):
	return [make_aware(datetime.datetime.strptime(x, '%Y-%m-%d')) for x in range.split(' to ')]

def get_sentinel_date():
	return make_aware(datetime.datetime.strptime('9999-12-31', '%Y-%m-%d'))

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

def datediff_hours(delta):
	days, seconds = delta.days, delta.seconds
	return days * 24 + seconds // 3600

def get_date_overlap(range1, range2):
	latest_start = max(range1[0], range2[0])
	earliest_end = min(range1[1], range2[1])
	delta = (earliest_end - latest_start) # + datetime.timedelta(days=1)
	return delta if delta.total_seconds() > 0 else datetime.timedelta()
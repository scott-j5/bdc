import datetime
import re

from django.utils.timezone import make_aware

#Attempts to find a matching date string format for use in strptime
def strp_ambiguous_date(date_string):
	if date_string:
		patterns = (
			[r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z", "%Y-%m-%dT%H:%M:%S.%fZ"],
			[r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+", "%Y-%m-%dT%H:%M:%S.%f"],
			[r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", "%Y-%m-%dT%H:%M:%SZ"],
			[r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", "%Y-%m-%dT%H:%M:%S"],
			[r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}Z", "%Y-%m-%dT%H:%MZ"],
			[r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}", "%Y-%m-%dT%H:%M"],
			[r"\d{4}-\d{2}-\d{2}T\d{2}Z", "%Y-%m-%dT%HZ"],
			[r"\d{4}-\d{2}-\d{2}T\d{2}", "%Y-%m-%dT%H"],
			[r"\d{4}-\d{2}-\d{2}Z", "%Y-%m-%dZ"],
			[r"\d{4}-\d{2}-\d{2}", "%Y-%m-%d"],
		)
		
		for pattern, format_str in patterns:
			match = re.match(pattern, date_string)
			if match:
				return datetime.datetime.strptime(date_string, format_str)
	
	return False

def parse_date(date):
	return make_aware(strp_ambiguous_date(date)) if date else False

def parse_date_range(range):
	return [make_aware(strp_ambiguous_date(x)) for x in range.split(' to ')] if range else [False, False]

def get_sentinel_date():
	return make_aware(datetime.datetime.strptime('9999-12-31', '%Y-%m-%d'))

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

def datediff_days(delta):
	days, seconds = delta.days, delta.seconds
	return days

def datediff_hours(delta):
	days, seconds = delta.days, delta.seconds
	return days * 24 + seconds // 3600

def get_date_overlap(range1, range2):
	latest_start = max(range1[0], range2[0])
	earliest_end = min(range1[1], range2[1])
	delta = (earliest_end - latest_start) # + datetime.timedelta(days=1)
	return delta if delta.total_seconds() > 0 else datetime.timedelta()
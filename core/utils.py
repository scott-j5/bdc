import datetime
import re
import decimal

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
	date_list = range.split(' to ') if len(range.split(' to ')) > 1 else [range.split(' to ')[0], range.split(' to ')[0]]
	return [make_aware(strp_ambiguous_date(x)) for x in date_list] if range else [False, False]

def parse_date_range_day_inclusive(range):
	dt_range = parse_date_range(range)
	if dt_range[0] == dt_range[1]:
		dt_range[0] = make_aware(datetime.datetime.combine(dt_range[0].date(), datetime.datetime.strptime('00:00', '%H:%M').time()))
		dt_range[1] = make_aware(datetime.datetime.combine(dt_range[1].date(), datetime.datetime.strptime('23:59', '%H:%M').time()))
	return dt_range

def get_sentinel_date():
	return make_aware(datetime.datetime.strptime('9999-12-31', '%Y-%m-%d'))

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

def datediff_days(delta):
	days, seconds = delta.days, delta.seconds
	delta_float = delta / datetime.timedelta(days=1)
	return decimal.Decimal(delta_float)

def datediff_hours(delta):
	days, seconds = delta.days, delta.seconds
	return days * 24 + seconds // 3600

def get_date_overlap(range1, range2):
	latest_start = max(range1[0], range2[0])
	earliest_end = min(range1[1], range2[1])
	delta = (earliest_end - latest_start) # + datetime.timedelta(days=1)
	return delta if delta.total_seconds() > 0 else datetime.timedelta()

def format_price(price, symbol=False):
	sym = symbol if symbol else "$"
	formatted_val = "{:.2f}".format(price) if price else ""
	return f"{sym}{formatted_val}"
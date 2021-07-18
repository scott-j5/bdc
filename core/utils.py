import datetime

def parse_date_range(range):
	return [datetime.datetime.strptime(x, '%Y-%m-%d') for x in range.split(' to ')]
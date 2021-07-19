import datetime

def parse_date_range(range):
	return [datetime.datetime.strptime(x, '%Y-%m-%d') for x in range.split(' to ')]

def get_sentinel_date():
	return datetime.datetime.strptime('9999-12-31', '%Y-%m-%d')

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)
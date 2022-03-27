import datetime

# Django library.
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

def retrieve(name):
    try:
        return getattr(settings, name, False)
    except ImproperlyConfigured:
        # To handle the auto-generation of documentations.
        return False

#Bool, If false, charges hourly
CHARGE_RENTAL_DAILY = retrieve('CHARGE_RENTAL_DAILY') or True

VERBOSE_CHARGE_PERIOD = 'night' if CHARGE_RENTAL_DAILY else 'hour'
VERBOSE_CHARGE_PERIOD_PLURAL = f"{VERBOSE_CHARGE_PERIOD}s"
VERBOSE_CHARGE_PERIOD_ADJ = f"{VERBOSE_CHARGE_PERIOD}ly"

#Minimum period for a rental
MINIMUM_RENTAL_PERIOD = retrieve('MINIMUM_RENTAL_PERIOD') or 3

#Check-in time
RENTAL_CHECK_IN_TIME = retrieve('RENTAL_CHECK_IN_TIME') or datetime.datetime.strptime('15:00', '%H:%M').time()
#Check-out time
RENTAL_CHECK_OUT_TIME = retrieve('RENTAL_CHECK_OUT_TIME') or datetime.datetime.strptime('11:00', '%H:%M').time()
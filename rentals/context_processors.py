from rentals.settings import SHORT_VERBOSE_CHARGE_PERIOD, VERBOSE_CHARGE_PERIOD

# Returns a verbose definition of the rental charge period
def charge_period(request):
	return { 
		"charge_period": SHORT_VERBOSE_CHARGE_PERIOD,
		"charge_period_plural": VERBOSE_CHARGE_PERIOD,
	}
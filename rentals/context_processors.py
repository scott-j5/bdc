from rentals.settings import VERBOSE_CHARGE_PERIOD, VERBOSE_CHARGE_PERIOD_ADJ, VERBOSE_CHARGE_PERIOD_PLURAL

# Returns a verbose definition of the rental charge period
def charge_period(request):
	return { 
		"charge_period": VERBOSE_CHARGE_PERIOD,
		"charge_period_plural": VERBOSE_CHARGE_PERIOD_PLURAL,
		"charge_period_adj": VERBOSE_CHARGE_PERIOD_ADJ,
	}
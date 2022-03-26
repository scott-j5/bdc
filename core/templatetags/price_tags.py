from django import template

from core.utils import format_price

register = template.Library()

# Formats an integer into a price to two decimal places
def price(value, arg=False):
	return format_price(value, arg)

register.filter('price', price)
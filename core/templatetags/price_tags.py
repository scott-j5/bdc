from django import template

register = template.Library()

# Formats an integer into a price to two decimal places
def price(value, arg=False):
	symbol = arg if arg else "$"
	formatted_val = "{:.2f}".format(value) if value else ""
	return f"{symbol}{formatted_val}"

register.filter('price', price)
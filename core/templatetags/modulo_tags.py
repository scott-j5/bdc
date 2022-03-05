from django import template

register = template.Library()

# Runs a modulus function on passed numbers
def modulo(num, val):
    return num % val

register.filter('modulo', modulo)
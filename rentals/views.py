from django.shortcuts import render
from django.views.generic import DetailView

from .models import ProductRental

# Create your views here.
def RentalDetailView(DetailView):
	model = ProductRental
	template_name = 'rentals/product_rental_detail.html'
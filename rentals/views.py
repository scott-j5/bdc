from core.forms import DateRangeFormMulti
from core.utils import parse_date_range
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import BadRequest
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from products.models import Product

from .models import ProductRental

# Create your views here.
class RentalPriceDetailView(UserPassesTestMixin, DetailView):
	model = ProductRental
	template_name = 'rentals/product_rental_detail.html'

	def test_func(self):
		return self.request.user.is_staff

	def get_object(self, *args, **kwargs):
		obj = get_object_or_404(Product, slug=self.kwargs['slug'])
		if obj.rentable == True:
			return obj
		else:
			raise BadRequest(_("The product selected is not available to rent!"))
			return None

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		unavailable = self.object.unavailable
		if self.request.GET:
			context["form"] = DateRangeFormMulti(self.request.GET, action=reverse_lazy("rental-price-detail", kwargs={'slug': self.object.slug}), submit_text="Change Dates", flatpickr_args={"disable":unavailable})
			if context["form"].is_valid():
				dates = parse_date_range(self.request.GET.get('stay'))
				context["rental"] = ProductRental(user=self.request.user, rental_product=self.object, rental_start=dates[0], rental_end=dates[1])
		else:
			context["form"] = DateRangeForm(action=reverse_lazy("van-detail", kwargs={'slug': self.object.slug}), submit_text="Check Pricing", flatpickr_args={"disable":unavailable})
		return context


class RentalDetailView(DetailView):
	model = ProductRental
	template_name = 'rentals/product_rental_detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		unavailable = self.rental_product.unavailable
		if self.request.GET:
			context["form"] = DateRangeFormMulti(self.request.GET, action=reverse_lazy("product-rental-detail", kwargs={'slug': self.object.slug}), submit_text="Change Dates", flatpickr_args={"disable":unavailable})
			if context["form"].is_valid():
				dates = parse_date_range(self.request.GET.get('stay'))
				context["rental"] = ProductRental(user=self.request.user, rental_product=self.object, rental_start=dates[0], rental_end=dates[1])
		else:
			context["form"] = DateRangeForm(action=reverse_lazy("van-detail", kwargs={'slug': self.object.slug}), submit_text="Check Pricing", flatpickr_args={"disable":unavailable})
		return context
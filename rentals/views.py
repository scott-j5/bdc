from core.forms import DateRangeFormMulti
from core.utils import parse_date_range
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import BadRequest
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView
from products.models import Product

from .forms import FuilfilmentDateRangeForm
from .models import RentalFulfilment

# Create your views here.
class RentalFulfilmentListView(UserPassesTestMixin, ListView):
	model = RentalFulfilment
	template_name = "rentals/rental_fulfilment_list.html"
	
	def test_func(self):
		return self.request.user.is_staff

	def get_queryset(self):
		user_id = self.kwargs.get('pk', self.request.user.id)
		return RentalFulfilment.objects.filter(rental_user__id=user_id)


class RentalFulfilmentDetailView(UserPassesTestMixin, DetailView):
	model = RentalFulfilment
	template_name = 'rentals/rental_fulfilment_detail.html'

	def test_func(self):
		return self.request.user.is_staff

	def get_object(self, *args, **kwargs):
		if self.kwargs.get('pk'):
			obj = get_object_or_404(RentalFulfilment, id=self.kwargs['pk'])
		else:
			slug = self.kwargs.get('slug') if self.kwargs.get('slug') else self.request.GET.get('product', "")
			# Return new dry instance
			product = get_object_or_404(Product, slug=slug)
			if product.rentable == True:
				form = FuilfilmentDateRangeForm(self.request.GET)
				if form.is_valid():
					fulfilment_date_time = form.cleaned_data['fulfilment_date_time'] if self.request.GET.get('fulfilment_date_time') else timezone.now()
					obj = RentalFulfilment(product=product, fulfilment_date_time=fulfilment_date_time, rental_start=form.cleaned_data['check_in'], rental_end=form.cleaned_data['check_out'])
			else:
				raise BadRequest(_("The product selected is not available to rent!"))
				return None
		return obj

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.object.id is None:
			form_action = reverse_lazy('rental-fulfilment-detail', kwargs={'slug': self.object.product.slug})
			if self.request.GET:
				context["form"] = FuilfilmentDateRangeForm(self.request.GET, action=form_action, submit_text="Change Dates", flatpickr_args={"disable":[]})
				context["form"].full_clean()
			else:
				context["form"] = FuilfilmentDateRangeForm(action=form_action, submit_text="Check Pricing", flatpickr_args={"disable":unavailable})
		return context


class MyRentals(UserPassesTestMixin, ListView):
	model = RentalFulfilment
	template_name = "rentals/my_rentals.html"

	def test_func(self):
		return self.request.user.is_authenticated

	def get_queryset(self, *args, **kwargs):
		#If no user id is provided default to request.user
		if not self.kwargs.get('pk', False):
			self.kwargs['user_set'] = True
			self.kwargs['pk'] = self.request.user.id
		return RentalFulfilment.objects.filter(rental_user__id=self.kwargs['pk'])

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		user_id = self.kwargs.get('pk', self.request.user.id)
		context['base_user'] = {"user": User.objects.get(id=user_id)}
		return context
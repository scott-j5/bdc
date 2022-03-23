from core.forms import DateRangeForm, DateRangeFormMulti
from core.utils import parse_date_range

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView

from products.models import ProductFulfilment
from products.views import CompleteProductUpdateView, ProductDeleteView
from rentals.models import RentalFulfilment, RentalRules, RentalInformation
from rentals.forms import RentalFulfilmentCreateForm, RentalDateRangeForm

from .models import (
	Van,
)

# Create your views here.
class VanListView(ListView):
	model = Van
	template_name = 'vans/van_list.html'

	def get_queryset(self):
		if self.request.GET:
			form = DateRangeFormMulti(self.request.GET)
			if form.is_valid():
				qs = Van.objects.available().get_prices([form.cleaned_data["check_in"], form.cleaned_data["check_out"]])
		else:
			qs = Van.objects.all()
		return qs

	#Get nearby stays of similar length!
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.request.GET:
			context["form"] = DateRangeFormMulti(self.request.GET, action=reverse_lazy("van-list"), submit_text="Change Dates", flatpickr_args={})
			if context["form"].is_valid() and len(self.object_list) <= 0:
				context['alt_rentals'] = Van.objects.nearby([context["form"].cleaned_data['check_in'], context["form"].cleaned_data['check_out']])
		else:
			context["form"] = DateRangeFormMulti(action=reverse_lazy("van-list"), submit_text="Check Pricing", flatpickr_args={})
		return context


class VanDetailView(DetailView):
	model = Van
	template_name = 'vans/van_detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["rental_information"] = RentalInformation.objects.all()
		context["rental_rules"] = RentalRules.objects.all()
		if self.request.GET:
			context["form"] = RentalDateRangeForm(self.request.GET, action=reverse_lazy("van-detail", kwargs={'slug': self.object.slug}), submit_text="Change Dates", flatpickr_args={"disable":self.object.flatpickr_unavailable})
			if context["form"].is_valid():
				fulfilment_date_time = timezone.make_aware(datetime.datetime.strptime(self.request.GET.get('fulfilment_date'), '%Y-%m-%d')) if self.request.GET.get('fulfilment_date') else timezone.now()
				rental_dates = [context['form'].cleaned_data['check_in'], context['form'].cleaned_data['check_out']] 
				context["rental_fulfilment"] = RentalFulfilment(product=self.object, fulfilment_date_time=fulfilment_date_time, rental_start=context['form'].cleaned_data['check_in'], rental_end=context['form'].cleaned_data['check_out'])
				context["rental_create_form"] = RentalFulfilmentCreateForm(instance=context["rental_fulfilment"])
		else:
			context["form"] = RentalDateRangeForm(action=reverse_lazy("van-detail", kwargs={'slug': self.object.slug}), submit_text="Check Pricing", flatpickr_args={"disable":self.object.flatpickr_unavailable})
		return context


class VanUpdateView(PermissionRequiredMixin, CompleteProductUpdateView):
	permission_required = 'van.change_van'
	raise_exception = True



class VanDeleteView(ProductDeleteView):
	pass
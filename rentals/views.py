from core.forms import DateRangeFormMulti
from core.utils import parse_date_range
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import BadRequest
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, FormView, UpdateView
from products.models import Product

from .forms import (
	AdminRentalFulfilmentCreateForm,
	RentalDriverFormSet,
	RentalDriverFormsetHelper,
	RentalFuilfilmentDateRangeForm,
	RentalFulfilmentCreateForm,
	RentalFulfilmentExtrasForm
)
from .models import RentalDriver, RentalFulfilment

# Create your views here.
class RentalFulfilmentListView(UserPassesTestMixin, ListView):
	model = RentalFulfilment
	template_name = "rentals/rental_fulfilment_list.html"
	
	def test_func(self):
		return self.request.user.is_staff

	def get_queryset(self):
		user_id = self.kwargs.get('pk', self.request.user.id)
		return RentalFulfilment.objects.filter(fulfilling_user__id=user_id)


class RentalFulfilmentPriceCheckView(UserPassesTestMixin, DetailView):
	model = RentalFulfilment
	template_name = 'rentals/rental_fulfilment_price_check.html'

	def test_func(self):
		return self.request.user.is_staff

	def get_object(self, *args, **kwargs):
		if self.kwargs.get('pk'):
			obj = get_object_or_404(RentalFulfilment, id=self.kwargs['pk'])
		else:
			slug = self.kwargs.get('slug') if self.kwargs.get('slug') else self.request.GET.get('product', "")
			# Return new dry instance
			product = get_object_or_404(Product, slug=slug)
			try:
				product.rentalproduct
				form = RentalFuilfilmentDateRangeForm(self.request.GET)
				if form.is_valid():
					fulfilment_date_time = form.cleaned_data['fulfilment_date_time'] if self.request.GET.get('fulfilment_date_time') else timezone.now()
					obj = RentalFulfilment(product=product, fulfilment_date_time=fulfilment_date_time, rental_start=form.cleaned_data['check_in'], rental_end=form.cleaned_data['check_out'])
			except:
				raise BadRequest(_("The product selected is not available to rent!"))
				return None
		return obj
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.object.id is None:
			form_action = reverse_lazy('rental-fulfilment-detail', kwargs={'slug': self.object.product.slug})
			if self.request.GET:
				context["form"] = RentalFuilfilmentDateRangeForm(self.request.GET, action=form_action, submit_text="Change Dates", flatpickr_args={"disable":self.object.product.rentalproduct.flatpickr_unavailable})
				context["form"].full_clean()
			else:
				context["form"] = RentalFuilfilmentDateRangeForm(action=form_action, submit_text="Check Pricing", flatpickr_args={"disable":self.object.product.rentalproduct.flatpickr_unavailable})
		return context


class RentalFulfilmentDetailView(UserPassesTestMixin, DetailView):
	model = RentalFulfilment
	template_name = 'rentals/rental_fulfilment_detail.html'

	def test_func(self):
		if self.kwargs.get('pk'):
			if self.request.user == self.get_object().fulfilling_user:
				return True
		if self.request.user.is_staff:
			return True
		return False

	def get_object(self, *args, **kwargs):
		if self.kwargs.get('pk'):
			obj = get_object_or_404(RentalFulfilment, id=self.kwargs['pk'])
		else:
			slug = self.kwargs.get('slug') if self.kwargs.get('slug') else self.request.GET.get('product', "")
			# Return new dry instance
			product = get_object_or_404(Product, slug=slug)
			try:
				product.rentalproduct
				form = RentalFuilfilmentDateRangeForm(self.request.GET)
				if form.is_valid():
					fulfilment_date_time = form.cleaned_data['fulfilment_date_time'] if self.request.GET.get('fulfilment_date_time') else timezone.now()
					obj = RentalFulfilment(product=product, fulfilment_date_time=fulfilment_date_time, rental_start=form.cleaned_data['check_in'], rental_end=form.cleaned_data['check_out'])
			except:
				raise BadRequest(_("The product selected is not available to rent!"))
				return None
		return obj

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.object.id is None:
			form_action = reverse_lazy('rental-fulfilment-detail', kwargs={'slug': self.object.product.slug})
			if self.request.GET:
				context["form"] = RentalFuilfilmentDateRangeForm(self.request.GET, action=form_action, submit_text="Change Dates", flatpickr_args={"disable":self.object.product.rentalproduct.flatpickr_unavailable})
				context["form"].full_clean()
			else:
				context["form"] = RentalFuilfilmentDateRangeForm(action=form_action, submit_text="Check Pricing", flatpickr_args={"disable":self.object.product.rentalproduct.flatpickr_unavailable})
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
		return RentalFulfilment.objects.filter(fulfilling_user__id=self.kwargs['pk'])

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		user_id = self.kwargs.get('pk', self.request.user.id)
		context['usr'] = User.objects.get(id=user_id)
		return context


class RentalFulfilmentTerms(LoginRequiredMixin, FormView):
	form_class = RentalFulfilmentCreateForm
	template_name = 'rentals/rental_terms.html'

	def get_form_kwargs(self, *args, **kwargs):
		args = super().get_form_kwargs(*args, **kwargs)
		args.update({
			'hidden': True,
		})
		return args

	def get_initial(self, *args, **kwargs):
		initial = super().get_initial(*args, **kwargs)
		initial.update(self.request.GET.dict())
		return initial


class RentalFulfilmentCreateView(LoginRequiredMixin, CreateView):
	model = RentalFulfilment
	template_name = 'rentals/rental_add.html'

	def get_form_class(self, *args, **kwargs):
		if self.request.user.is_staff:
			return AdminRentalFulfilmentCreateForm
		else:
			return RentalFulfilmentCreateForm

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()

		kwargs.update({
			'request': self.request,
		})
		return kwargs

	def form_valid(self, form):
		if not self.request.user.is_staff:
			form.instance.fulfilling_user = self.request.user
		return super().form_valid(form)

	def get_success_url(self):
		return reverse_lazy('rental-fulfilment-extras', kwargs={'pk': self.object.id,})


class RentalFulfilmentConfirmExtras(UserPassesTestMixin, UpdateView):
	model = RentalFulfilment
	form_class = RentalFulfilmentExtrasForm
	template_name = 'rentals/rental_confirm_extras.html'

	def test_func(self):
		obj = self.get_object()
		return obj.fulfilling_user == self.request.user or self.request.user.is_staff

	def get_success_url(self):
		return reverse_lazy('rental-fulfilment-drivers', kwargs={'pk': self.object.id,})


class RentalFulfilmentConfirmDrivers(UserPassesTestMixin, FormView):
	form_class = RentalDriverFormSet
	template_name = 'rentals/rental_confirm_details.html'

	def test_func(self):
		obj = self.get_object()
		return obj.fulfilling_user == self.request.user or self.request.user.is_staff

	def get_object(self):
		self.object = get_object_or_404(RentalFulfilment, pk=self.kwargs.get('pk'))
		return self.object

	def get_context_data(self, *args, **kwargs):
		ctx = super().get_context_data(*args, **kwargs)
		ctx.update({
			'object': self.get_object(),
			'helper': RentalDriverFormsetHelper(rental_fulfilment_id=self.object.id),
		})
		return ctx

	def form_valid(self, form):
		self.form = form
		return HttpResponseRedirect(self.get_success_url())

	def get_success_url(self):
		if self.request.user.is_staff and self.request.user:
			return reverse_lazy('my-rentals')
		return reverse_lazy('my-rentals')
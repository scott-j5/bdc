import datetime

from allauth.account.models import EmailAddress
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import CreateView, ListView, DetailView


from rentals.models import RentalFulfilment, RentalDriver

# Create your views here.

def dashboard_view(request):
	if request.user.is_staff:
		users_count = User.objects.all().count()
		completed_rentals_ytd = RentalFulfilment.objects.filter(Q(rental_start__gt=datetime.datetime.strptime(f'01/01/{datetime.datetime.now().year}', '%d/%m/%Y')), Q(rental_start__lt=timezone.now()), ~Q(status=RentalFulfilment.Status.DENIED)).count()
		pending_rentals_count = RentalFulfilment.objects.filter(rental_start__gt=timezone.now()).count()
		drivers_requiring_approval_count = RentalDriver.objects.filter(Q(status=RentalDriver.Status.AWAITING_REVIEW) | Q(status=RentalDriver.Status.ACTION_REQUIRED)).count()
		upcoming_rentals = RentalFulfilment.objects.filter(Q(rental_start__gte=timezone.now()), ~Q(status=RentalDriver.Status.DENIED)).order_by('-rental_start')[:4]
		
		ctx = {
			'users_count': users_count,
			'completed_rentals_ytd': completed_rentals_ytd,
			'pending_rentals_count': pending_rentals_count,
			'drivers_requiring_approval_count': drivers_requiring_approval_count,
			'upcoming_rentals': upcoming_rentals,
		}
		return render(request, 'dashboard/dashboard_index.html', ctx)
	return PermissionDenied()


class UsersListView(UserPassesTestMixin, ListView):
	model = User
	template_name = 'dashboard/user_list.html'
	rasie_exception = True

	def test_func(self):
		if self.request.user.is_staff:
			return True
		return False

	def get_context_data(self, *args, **kwargs):
		ctx = super().get_context_data(*args, *kwargs)
		users_count = User.objects.all().count()
		new_users_count = User.objects.filter(date_joined__gte=datetime.datetime.strptime(f'01/{datetime.datetime.now().month}/{datetime.datetime.now().year}', '%d/%m/%Y')).count()
		user_growth = new_users_count / users_count * 100
		users_verified_count = EmailAddress.objects.filter(verified=True).distinct('user').count()
		users_booked_count = RentalFulfilment.objects.filter(~Q(status=RentalFulfilment.Status.DENIED)).distinct('fulfilling_user').count()
		users_booked_percent = users_booked_count / users_count * 100

		ctx.update({
			'users_count': users_count,
			'new_users_count': new_users_count,
			'user_growth': user_growth,
			'users_verified_count': users_verified_count,
			'users_booked_percent': users_booked_percent,
		})
		return ctx

class RentalsListView(UserPassesTestMixin, ListView):
	model = RentalFulfilment
	template_name = 'dashboard/rental_list.html'
	rasie_exception = True

	def test_func(self):
		if self.request.user.is_staff:
			return True
		return False


class DriversListView(UserPassesTestMixin, ListView):
	model = RentalDriver
	template_name = 'dashboard/driver_list.html'
	rasie_exception = True

	def test_func(self):
		if self.request.user.is_staff:
			return True
		return False
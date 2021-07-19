from core.forms import DateRangeForm
from core.utils import parse_date_range
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from rentals.models import Reservation

from rentals.models import ProductRental

from .models import (
	Van,
)

# Create your views here.
class VanListView(ListView):
	model = Van
	template_name = 'vans/van_list.html'

	def get_queryset(self):
		qs = Van.objects.filter()
		return qs

	#get nearby stays of similar length
	def get_context_data(self, **kwargs):
		pass

class VanDetailView(DetailView):
	model = Van
	template_name = 'vans/van_detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		unavailable = self.object.unavailable()
		if self.request.GET:
			context["form"] = DateRangeForm(self.request.GET, action=reverse_lazy("van-detail", kwargs={'slug': self.object.slug}), submit_text="Change Dates", flatpickr_args={"disable":unavailable})
			if context["form"].is_valid():
				dates = parse_date_range(self.request.GET.get('stay'))
				context["rental"] = ProductRental(user=self.request.user, product=self.object, rental_start=dates[0], rental_end=dates[1])
		else:
			context["form"] = DateRangeForm(action=reverse_lazy("van-detail", kwargs={'slug': self.object.slug}), submit_text="Check Pricing", flatpickr_args={"disable":unavailable})
		return context



def van_list(request):
	context = {
		"form" : DateRangeForm(action=revere_lazy("van-list", kwargs={'pk': 1}), flatpickr_args={"disable":["2021-07-20", "2021-07-21"]})
	}
	return render(request, 'vans/van_list.html', context)

def van_detail(request, slug):
	context = {}
	return render(request, 'vans/van_detail.html', context)
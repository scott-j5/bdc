from django.shortcuts import render

from blogs.models import Blog

from .forms import ContactForm, DateRangeForm, DateRangeFormMulti

# Create your views here.
def home_view(request):
	context = {
		"blogs": Blog.objects.filter(published=True).distinct().order_by('-published_on')[:3],
		"date_range_form": DateRangeFormMulti(action="van-list", flatpickr_args={"disable":["2021-07-20", "2021-07-21"]}),
		"contact_form": ContactForm()
	}
	return render(request, 'core/home.html', context)

def contact_view(request):
	context = {
		"contact_form": ContactForm()
	}
	return render(request, 'core/home.html', context)

def about_us_view(request):
	context = {}
	return render(request, 'core/about-us.html', context)

def pricing_view(request):
	context = {}
	return render(request, 'core/pricing.html', context)

def pre_booking_info_view(request):
	context = {}
	return render(request, 'core/pre_booking_info.html', context)

def pre_trip_checklist_view(request):
	context = {}
	return render(request, 'core/pre_trip_checklist.html', context)

def testimonials_view(request):
	context = {}
	return render(request, 'core/testimonials.html', context)

def error_403(request, exception):
	context = {}
	return render(request, 'core/403.html', context, status=403)

def error_404(request, exception):
	context = {}
	return render(request, 'core/404.html', context, status=404)

def error_500(request):
	context = {}
	return render(request, 'core/500.html', context, status=500)

def testemail_view(request):
	if request.user.is_staff:
		return render(request, 'core/email/base_email.html')
	else:
		return render(request, 'core/403.html', context, status=403)
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
    return render(request, 'core/pricing.html', context)

def pricing_view(request):
    context = {}
    return render(request, 'core/pricing.html', context)

def faqs_view(request):
    context = {
		"form": ContactForm()
	}
    return render(request, 'core/faqs.html', context)

def testimonials_view(request):
    context = {}
    return render(request, 'core/testimonials.html', context)

def error_403(request, exception):
    context = {}
    return render(request, 'core/403.html', context)


def error_404(request, exception):
    context = {}
    return render(request, 'core/404.html', context)

def error_500(request):
    context = {}
    return render(request, 'core/500.html', context)
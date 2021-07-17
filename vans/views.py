from django.shortcuts import render

from .models import (
	Van
)

# Create your views here.
def van_list(request):
	context = {}
	return render(request, 'vans/van_list.html', context)

def van_detail(request, slug):
	context = {}
	return render(request, 'vans/van_detail.html', context)
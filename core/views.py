from django.shortcuts import render

# Create your views here.
def home_view(request):
    context = {}
    return render(request, 'core/home.html', context)

def vans_view(request):
    context = {}
    return render(request, 'core/vans.html', context)
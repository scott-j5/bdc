"""bdc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler403, handler404, handler500

from core.views import (
	error_403,
	error_404,
	error_500,
)

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
	path('accounts/', include('accounts.urls')),
	path('blogs/', include('blogs.urls')),
	path('dashboard/', include('dashboard.urls')),
	path('djrichtextfield/', include('djrichtextfield.urls')),
	path('faqs/', include('faq.urls')),
	path('rentals/', include('rentals.urls')),
	path('vans/', include('vans.urls')),
]

handler403 = error_403
handler404 = error_404
handler500 = error_500
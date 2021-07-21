from django.urls import path, include

from .views import (
	RentalPriceDetailView,
	RentalDetailView
)

urlpatterns = [
    path('<slug:slug>/', RentalPriceDetailView.as_view(), name='rental-price-detail'),
	path('<int:pk>/', RentalDetailView.as_view(), name='rental-detail'),
]

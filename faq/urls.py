from django.urls import path, include

from .views import (
	faqs_view,
	FaqCreateView,
	FaqUpdateView,
	FaqDeleteView,
	FaqCategoryCreateView,
	FaqCategoryUpdateView,
)

urlpatterns = [
    path('', faqs_view, name='faqs'),
	path('add/', FaqCreateView.as_view(), name='faq-add'),
	path('add/to-category/<int:pk>/', FaqCreateView.as_view(), name='faq-add'),
	path('<int:pk>/update/', FaqUpdateView.as_view(), name='faq-update'),
	path('<int:pk>/delete/', FaqDeleteView.as_view(), name='faq-delete'),
	path('category/add/', FaqCategoryCreateView.as_view(), name='faq-category-add'),
	path('category/<int:pk>/update/', FaqCategoryUpdateView.as_view(), name='faq-category-update'),
]
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView


from .forms import ProductForm, ProductFeatureFormSet, ProductImageFormSet, ProductFeatureFormHelper, ProductImageFormHelper
from .models import Product, ProductFeature, ProductImage, Review

# Create your views here.
class ProductImageDetailView(DetailView):
	model = ProductImage
	template_name = "product/productimage_detail.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["images"] = ProductImage.object.filter(product=self.object.product).order_by('id')
		return context


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
	permission_required = 'products.change_product'
	raise_exception = True
	model = Product
	form_class = ProductForm
	template_name = 'products/product_form.html'

	def get_success_url(self):
		return reverse('product-detail', kwargs={'slug': self.slug})


class CompleteProductUpdateView(PermissionRequiredMixin, UpdateView):
	permission_required = 'products.change_product'
	raise_exception = True
	model = Product
	form_class = ProductForm
	image_form_class = ProductImageFormSet
	feature_form_class = ProductFeatureFormSet
	template_name = 'products/complete_product_form.html'

	def get_context_data(self, **kwargs):
		context = super(CompleteProductUpdateView, self).get_context_data(**kwargs)
		if 'form' not in context:
			context['form'] = self.form_class(instance=self.object)
		if 'image_form' not in context:
			context['image_form_helper'] = ProductImageFormHelper
			context['image_form'] = self.image_form_class(initial=ProductImage.objects.filter(product=self.object).values())
		if 'feature_form' not in context:
			context['feature_form_helper'] = ProductFeatureFormHelper
			context['feature_form'] = self.feature_form_class(initial=ProductFeature.objects.filter(product=self.object).values())
		return context


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
	permission_required = 'products.delete_product'
	raise_exception = True
	model = Product
	template_name = 'products/product_confirm_delete.html'
	success_url = reverse_lazy('home')


class ReviewDetailView(DetailView):
	model = Review
	template_name = ''


class ReviewListView(ListView):
	model = Review
	template_name = ''
	#get_queryset options for by_product, by_product_fulfilment, by_user

class ReviewCreateView(CreateView):
	model = Review
	template_name = ''
	#only available to fulfilling user


class ReviewUpdateView(UpdateView):
	model = Review
	template_name = ''
	# Only available to staff or fulfilling users if not published


class ReviewDeleteView(PermissionRequiredMixin, DeleteView):
	premission_required = 'products.delete_review'
	raise_exception = True
	model = Review
	template_name = ''
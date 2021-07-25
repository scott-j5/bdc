from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import ProductImage

# Create your views here.
class ProductImageDetailView(DetailView):
	model = ProducImage
	template_name = "product/productimage_detail.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["images"] = ProductImage.object.filter(product=self.object.product).order_by('id')
		return context
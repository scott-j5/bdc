from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from core.forms import ContactForm

from .forms import FaqForm, FaqCategoryForm
from .models import Faq, FaqCategory

# Create your views here.
def faqs_view(request):
	context = {
		"faqs": Faq.objects.all(),
		"faq_categories": FaqCategory.objects.all(),
		"form": ContactForm()
	}
	return render(request, 'faq/faqs.html', context)


class FaqCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
	model = Faq
	permission_required = 'faq.add_faq'
	raise_exception = True
	template_name = 'faq/faq_form.html'
	success_url = reverse_lazy('faqs')
	form_class = FaqForm

	def get_form_kwargs(self, *args, **kwargs):
		kwargs = super().get_form_kwargs(*args, **kwargs)
		category_id = self.kwargs.get('pk', None)
		if category_id is not None:
			kwargs.update({
				'initial': {'category': self.kwargs.get('pk', None)},
			})
		return kwargs

	def get_success_message(self, cleaned_data):
		return f"FAQ '{ cleaned_data.get('title') }' was added."


class FaqUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
	model = Faq
	permission_required = 'faq.change_faq'
	raise_exception = True
	template_name = 'faq/faq_form.html'
	success_url = reverse_lazy('faqs')
	form_class = FaqForm

	def get_success_message(self, cleaned_data):
		return f"FAQ '{ cleaned_data.get('title') }' was updated."


class FaqDeleteView(PermissionRequiredMixin, DeleteView):
	model = Faq
	permission_required = 'faq.delete_faq'
	raise_exception = True
	template_name = 'faq/faq_confirm_delete.html'
	success_url = reverse_lazy('faqs')

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, self.get_success_message())
		return super().delete(request, *args, **kwargs)

	def get_success_message(self):
		obj = self.get_object()
		return f"FAQ '{ obj.title }' was deleted."


class FaqCategoryCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
	model = FaqCategory
	permission_required = 'faq.add_faqcategory'
	raise_exception = True
	template_name = 'faq/faqcategory_form.html'
	success_url = reverse_lazy('faqs')
	form_class = FaqCategoryForm

	def get_success_message(self, cleaned_data):
		return f"FAQ Category'{ cleaned_data.get('name') }' was added."


class FaqCategoryUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
	model = FaqCategory
	permission_required = 'faq.change_faqcategory'
	raise_exception = True
	template_name = 'faq/faqcategory_form.html'
	success_url = reverse_lazy('faqs')
	form_class = FaqCategoryForm

	def get_success_message(self, cleaned_data):
		return f"FAQ Category '{ cleaned_data.get('name') }' was updated."
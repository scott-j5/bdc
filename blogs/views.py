# Create your views here.
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core import serializers
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import FileResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, UpdateView
from django.views.generic.edit import BaseFormView


from .forms import BlogImageForm, BlogForm
from .models import Blog, BlogImage, Series, Tag


# Create your views here.
class BlogDetail(DetailView):
	model = Blog

	def get_object(self, **kwargs):
		obj = super().get_object(**kwargs)
		obj.increment_views()
		return obj


class BlogDelete(PermissionRequiredMixin, DeleteView):
	permission_required = 'blogs.delete_blog'
	model = Blog
	success_url = reverse_lazy('blog-list')


class BlogUpdate(PermissionRequiredMixin, UpdateView):
	permission_required = 'blogs.change_blog'
	raise_exception = True
	model = Blog
	form_class = BlogForm
	success_url = reverse_lazy('blog-list')


def blog_list(request):
	context = {}
	params = request.GET.dict()

	# Parse GET tags to list
	if request.GET.get('tags'):
		params['tags'] = [x for x in params['tags'].split(',') if len(x) >= 1]
	blogs = Blog.dict_filter(params)

	# Hide unplublished blogs except for the autoring user
	if not request.user.is_anonymous:
		blogs = blogs.filter(Q(published=True) | Q(author=request.user)).distinct()
	else:
		blogs = blogs.filter(published=True).distinct()
	
	context["blogs"] = blogs
	context["tags"] = Tag.objects.all()

	if request.content_type == 'application/json':
		response = serializers.serialize('json', blogs)
		return JsonResponse(response, safe=False)
	else:
		paginator = Paginator(context["blogs"], 12)
		page_number = request.GET.get('page')
		context["page_obj"] = paginator.get_page(page_number)

		if request.content_type == 'text/html':
			return render(request, 'blogs/blog_card_list.html', context)
		else:
			return render(request, 'blogs/blog_list.html', context)


def blog_image(request, *args, **kwargs):
	if kwargs.get('pk'):
		try:
			blog_image = BlogImage.objects.get(id=kwargs.get('pk'))
		except Exception as e:
			print(e)
			return False
	return redirect(blog_image.image.url)


class BlogImageUpload(BaseFormView):
	form_class = BlogImageForm
	success_url = '/'

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		blog_id = [x for x in self.request.META.get('HTTP_REFERER').split('/') if len(x) > 0][-2]
		blog_slug = Blog.objects.get(id=blog_id)
		if blog_slug:
			kwargs.update({'blog_slug': blog_slug.slug})
		return kwargs

	def form_invalid(self, form):
		if self.request.accepts('application/json') and not self.request.accepts('text/html'):
			return JsonResponse(form.errors, status=400)

		response = super().form_invalid(form)
		return response

	def form_valid(self, form):
		response = super().form_valid(form)

		if self.request.accepts('application/json') and not self.request.accepts('text/html'):
			image_path = form.save(commit=True)
			return JsonResponse({'location': image_path})
		return response

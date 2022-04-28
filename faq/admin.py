from django.contrib import admin

from .models import Faq, FaqCategory

# Register your models here.
admin.site.register(FaqCategory)
admin.site.register(Faq)
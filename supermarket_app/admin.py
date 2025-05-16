from django.contrib import admin
from .models import Market, Seller, Product

# Register your models here.
admin.site.register(Market),
admin.site.register(Seller),
admin.site.register(Product)

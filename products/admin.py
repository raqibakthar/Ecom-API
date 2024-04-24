from django.contrib import admin
from .models import *
# Register your models here.

class productAdmin(admin.ModelAdmin):
        list_display=('name','brand','countInStock','created_at','updated_at')

admin.site.register(Product,productAdmin)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(ShippingAddress)

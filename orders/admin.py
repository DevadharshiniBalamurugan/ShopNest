from django.contrib import admin
from .models import Order,OrderItem,Payment,ShippingAddress
class OrderItemInline(admin.TabularInline): model=OrderItem; extra=0
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin): list_display=['number','user','status','payment_method','total','created_at']; list_filter=['status','payment_method']; search_fields=['number','user__username']; inlines=[OrderItemInline]
admin.site.register(Payment); admin.site.register(ShippingAddress)

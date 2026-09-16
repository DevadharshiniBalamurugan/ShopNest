from django.contrib import admin
from .models import Category,Brand,Seller,Product,ProductImage,ProductVariant,Wishlist,WishlistItem,Review,Coupon,NewsletterSubscriber
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['name','category','brand','price','stock','is_active']; list_filter=['category','brand','is_active']; search_fields=['name','sku']; prepopulated_fields={'slug':('name',)}
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin): prepopulated_fields={'slug':('name',)}
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin): prepopulated_fields={'slug':('name',)}
for model in [Seller,ProductImage,ProductVariant,Wishlist,WishlistItem,Review,Coupon,NewsletterSubscriber]: admin.site.register(model)

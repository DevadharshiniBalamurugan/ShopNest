from django.urls import path
from . import views
app_name='dashboard'
urlpatterns=[path('admin/',views.admin_dashboard,name='admin'),path('seller/register/',views.seller_register,name='seller_register'),path('seller/',views.seller_dashboard,name='seller'),path('seller/products/add/',views.product_form,name='product_add'),path('seller/products/<int:pk>/edit/',views.product_form,name='product_edit'),path('seller/products/<int:pk>/delete/',views.product_delete,name='product_delete')]

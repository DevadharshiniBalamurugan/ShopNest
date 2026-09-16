from django.urls import path
from . import views
app_name='orders'
urlpatterns=[path('checkout/',views.checkout,name='checkout'),path('success/<str:number>/',views.success,name='success'),path('',views.order_list,name='list'),path('<str:number>/',views.order_detail,name='detail'),path('<str:number>/track/',views.track,name='track'),path('<str:number>/cancel/',views.cancel,name='cancel')]

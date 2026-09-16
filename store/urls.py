from django.urls import path
from . import views
app_name='store'
urlpatterns=[path('',views.home,name='home'),path('products/',views.products,name='products'),path('search/',views.products,name='search'),path('categories/',views.categories,name='categories'),path('product/<slug:slug>/',views.product_detail,name='product_detail'),
path('cart/',views.cart_detail,name='cart'),path('cart/add/<int:pk>/',views.cart_add,name='cart_add'),path('cart/update/<int:pk>/',views.cart_update,name='cart_update'),path('cart/remove/<int:pk>/',views.cart_remove,name='cart_remove'),path('coupon/apply/',views.coupon_apply,name='coupon_apply'),path('coupon/remove/',views.coupon_remove,name='coupon_remove'),
path('wishlist/',views.wishlist,name='wishlist'),path('wishlist/toggle/<int:pk>/',views.wishlist_toggle,name='wishlist_toggle'),path('wishlist/move/<int:pk>/',views.wishlist_move,name='wishlist_move'),path('product/<slug:slug>/review/',views.review_save,name='review_save'),path('review/<int:pk>/delete/',views.review_delete,name='review_delete'),path('newsletter/',views.newsletter,name='newsletter'),
path('about/',views.info_page,{'page':'about'},name='about'),path('contact/',views.info_page,{'page':'contact'},name='contact'),path('privacy/',views.info_page,{'page':'privacy'},name='privacy'),path('terms/',views.info_page,{'page':'terms'},name='terms')]

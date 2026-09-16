from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
app_name='accounts'
urlpatterns=[
 path('register/',views.register,name='register'),path('login/',auth_views.LoginView.as_view(template_name='accounts/login.html'),name='login'),path('logout/',auth_views.LogoutView.as_view(),name='logout'),
 path('password-reset/',auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),name='password_reset'),
 path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),name='password_reset_done'),
 path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),name='password_reset_confirm'),
 path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),name='password_reset_complete'),
 path('profile/',views.profile,name='profile'),path('profile/edit/',views.edit_profile,name='edit_profile'),path('addresses/',views.addresses,name='addresses'),
 path('addresses/add/',views.address_form,name='address_add'),path('addresses/<int:pk>/edit/',views.address_form,name='address_edit'),path('addresses/<int:pk>/delete/',views.address_delete,name='address_delete'),path('addresses/<int:pk>/default/',views.address_default,name='address_default')]

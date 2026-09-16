from django.conf import settings
from django.db import models

class Profile(models.Model):
    ROLE_CHOICES=[('customer','Customer'),('seller','Seller')]
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='profile')
    role=models.CharField(max_length=12,choices=ROLE_CHOICES,default='customer',db_index=True)
    phone=models.CharField(max_length=20,blank=True)
    avatar=models.ImageField(upload_to='avatars/',blank=True)
    bio=models.CharField(max_length=240,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.user.username

class Address(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='addresses')
    full_name=models.CharField(max_length=120); phone=models.CharField(max_length=20)
    address=models.CharField(max_length=240); city=models.CharField(max_length=80)
    state=models.CharField(max_length=80); postal_code=models.CharField(max_length=15)
    country=models.CharField(max_length=80,default='India'); is_default=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-is_default','-created_at']
    def __str__(self): return f'{self.full_name} — {self.city}'

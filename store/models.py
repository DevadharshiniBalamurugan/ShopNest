from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator,MaxValueValidator
from django.db import models
from django.urls import reverse

class Category(models.Model):
    name=models.CharField(max_length=80,unique=True); slug=models.SlugField(unique=True)
    icon=models.CharField(max_length=8,default='✦'); description=models.CharField(max_length=180,blank=True)
    is_active=models.BooleanField(default=True)
    class Meta: verbose_name_plural='Categories'; ordering=['name']
    def __str__(self): return self.name

class Brand(models.Model):
    name=models.CharField(max_length=80,unique=True); slug=models.SlugField(unique=True)
    def __str__(self): return self.name

class Seller(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='seller_profile')
    store_name=models.CharField(max_length=120); description=models.TextField(blank=True)
    approved=models.BooleanField(default=False); created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.store_name

class Product(models.Model):
    name=models.CharField(max_length=180,db_index=True); slug=models.SlugField(unique=True)
    description=models.TextField(); specifications=models.JSONField(default=dict,blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(0)])
    original_price=models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    category=models.ForeignKey(Category,on_delete=models.PROTECT,related_name='products')
    brand=models.ForeignKey(Brand,on_delete=models.PROTECT,related_name='products')
    seller=models.ForeignKey(Seller,on_delete=models.SET_NULL,null=True,blank=True,related_name='products')
    sku=models.CharField(max_length=40,unique=True); stock=models.PositiveIntegerField(default=0,db_index=True)
    main_image=models.URLField(blank=True); image=models.ImageField(upload_to='products/',blank=True)
    rating=models.DecimalField(max_digits=2,decimal_places=1,default=0,validators=[MinValueValidator(0),MaxValueValidator(5)],db_index=True)
    is_active=models.BooleanField(default=True,db_index=True); is_featured=models.BooleanField(default=False)
    is_best_seller=models.BooleanField(default=False); created_at=models.DateTimeField(auto_now_add=True,db_index=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=['-created_at']; indexes=[models.Index(fields=['category','is_active']),models.Index(fields=['price','rating'])]
    def __str__(self): return self.name
    def get_absolute_url(self): return reverse('store:product_detail',args=[self.slug])
    @property
    def discount_percentage(self):
        if self.original_price and self.original_price > self.price: return round((self.original_price-self.price)*100/self.original_price)
        return 0
    @property
    def image_url(self): return self.image.url if self.image else self.main_image

class ProductImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images'); image=models.ImageField(upload_to='products/gallery/')
    alt_text=models.CharField(max_length=120,blank=True); sort_order=models.PositiveSmallIntegerField(default=0)

class ProductVariant(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='variants')
    name=models.CharField(max_length=40); value=models.CharField(max_length=80); stock=models.PositiveIntegerField(default=0)
    price_adjustment=models.DecimalField(max_digits=8,decimal_places=2,default=0)
    class Meta: constraints=[models.UniqueConstraint(fields=['product','name','value'],name='unique_product_variant')]

class Wishlist(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='wishlist')
    products=models.ManyToManyField(Product,through='WishlistItem')
class WishlistItem(models.Model):
    wishlist=models.ForeignKey(Wishlist,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE); added_at=models.DateTimeField(auto_now_add=True)
    class Meta: constraints=[models.UniqueConstraint(fields=['wishlist','product'],name='unique_wishlist_item')]

class Review(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='reviews')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    rating=models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    title=models.CharField(max_length=100); body=models.TextField(); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: constraints=[models.UniqueConstraint(fields=['user','product'],name='unique_product_review')]; ordering=['-created_at']

class Coupon(models.Model):
    TYPES=[('percent','Percentage'),('fixed','Fixed amount')]
    code=models.CharField(max_length=30,unique=True); discount_type=models.CharField(max_length=10,choices=TYPES)
    discount_value=models.DecimalField(max_digits=8,decimal_places=2); minimum_order=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    maximum_discount=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    start_date=models.DateTimeField(); expiry_date=models.DateTimeField(); usage_limit=models.PositiveIntegerField(default=100); times_used=models.PositiveIntegerField(default=0)
    is_active=models.BooleanField(default=True)
    def calculate(self,subtotal):
        value=subtotal*self.discount_value/Decimal('100') if self.discount_type=='percent' else self.discount_value
        return min(value,self.maximum_discount) if self.maximum_discount else value

class NewsletterSubscriber(models.Model):
    email=models.EmailField(unique=True); created_at=models.DateTimeField(auto_now_add=True)

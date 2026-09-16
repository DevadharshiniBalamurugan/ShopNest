import uuid
from django.conf import settings
from django.db import models
from store.models import Product,Coupon

class Order(models.Model):
    STATUSES=[('placed','Order Placed'),('confirmed','Confirmed'),('packed','Packed'),('shipped','Shipped'),('out','Out for Delivery'),('delivered','Delivered'),('cancelled','Cancelled')]
    PAYMENT=[('cod','Cash on Delivery'),('card','Card (Demo)'),('upi','UPI (Demo)')]
    number=models.CharField(max_length=18,unique=True,editable=False); user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='orders')
    status=models.CharField(max_length=16,choices=STATUSES,default='placed',db_index=True); payment_method=models.CharField(max_length=10,choices=PAYMENT,default='cod')
    subtotal=models.DecimalField(max_digits=12,decimal_places=2); discount=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    delivery_fee=models.DecimalField(max_digits=8,decimal_places=2,default=0); tax=models.DecimalField(max_digits=10,decimal_places=2,default=0); total=models.DecimalField(max_digits=12,decimal_places=2)
    coupon=models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True,blank=True); created_at=models.DateTimeField(auto_now_add=True,db_index=True); updated_at=models.DateTimeField(auto_now=True)
    def save(self,*a,**kw):
        if not self.number: self.number='CTV-'+uuid.uuid4().hex[:10].upper()
        super().save(*a,**kw)
    def __str__(self): return self.number

class ShippingAddress(models.Model):
    order=models.OneToOneField(Order,on_delete=models.CASCADE,related_name='shipping_address')
    full_name=models.CharField(max_length=120); phone=models.CharField(max_length=20); address=models.CharField(max_length=240)
    city=models.CharField(max_length=80); state=models.CharField(max_length=80); postal_code=models.CharField(max_length=15); country=models.CharField(max_length=80)

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items'); product=models.ForeignKey(Product,on_delete=models.PROTECT,related_name='order_items')
    product_name=models.CharField(max_length=180); quantity=models.PositiveIntegerField(); price=models.DecimalField(max_digits=10,decimal_places=2)
    @property
    def total(self): return self.price*self.quantity

class Payment(models.Model):
    STATUSES=[('pending','Pending'),('paid','Paid'),('failed','Failed'),('refunded','Refunded')]
    order=models.OneToOneField(Order,on_delete=models.CASCADE,related_name='payment'); provider=models.CharField(max_length=30,default='demo')
    transaction_id=models.CharField(max_length=80,blank=True); amount=models.DecimalField(max_digits=12,decimal_places=2); status=models.CharField(max_length=10,choices=STATUSES,default='pending'); created_at=models.DateTimeField(auto_now_add=True)

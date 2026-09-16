from decimal import Decimal
from .models import Product,Coupon

class Cart:
    def __init__(self,request): self.session=request.session; self.data=self.session.setdefault('cart',{}); self.coupon_code=self.session.get('coupon')
    def add(self,product,quantity=1,override=False):
        key=str(product.pk); current=self.data.get(key,{'quantity':0}); current['quantity']=quantity if override else current['quantity']+quantity
        current['quantity']=max(1,min(current['quantity'],product.stock)); self.data[key]=current; self.save()
    def remove(self,product): self.data.pop(str(product.pk),None); self.save()
    def clear(self): self.session.pop('cart',None); self.session.pop('coupon',None); self.session.modified=True
    def save(self): self.session.modified=True
    def __len__(self): return sum(i['quantity'] for i in self.data.values())
    def items(self):
        products=Product.objects.filter(pk__in=self.data.keys()).select_related('category','brand')
        for product in products:
            quantity=self.data[str(product.pk)]['quantity']; yield {'product':product,'quantity':quantity,'total':product.price*quantity}
    @property
    def subtotal(self): return sum((i['total'] for i in self.items()),Decimal('0'))
    @property
    def coupon(self): return Coupon.objects.filter(code__iexact=self.coupon_code).first() if self.coupon_code else None
    @property
    def discount(self): return min(self.subtotal,self.coupon.calculate(self.subtotal)) if self.coupon else Decimal('0')
    @property
    def delivery(self): return Decimal('0') if self.subtotal>=999 or not self.data else Decimal('79')
    @property
    def tax(self): return (self.subtotal-self.discount)*Decimal('.05')
    @property
    def total(self): return self.subtotal-self.discount+self.delivery+self.tax

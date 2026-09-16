from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Sum,Count,F
from django.shortcuts import get_object_or_404,redirect,render
from accounts.models import Profile
from orders.models import Order,OrderItem
from store.models import Product,Seller,Category,Review,Coupon
from .forms import ProductForm,SellerForm

def staff_required(view): return user_passes_test(lambda u:u.is_staff,login_url='accounts:login')(view)
def seller_required(view):
    @login_required
    def wrapped(request,*a,**kw):
        if not hasattr(request.user,'seller_profile'): messages.error(request,'Create a seller profile first.'); return redirect('dashboard:seller_register')
        return view(request,*a,**kw)
    return wrapped

@staff_required
def admin_dashboard(request):
    orders=Order.objects.exclude(status='cancelled'); revenue=orders.aggregate(v=Sum('total'))['v'] or 0
    top=OrderItem.objects.values('product_name').annotate(units=Sum('quantity')).order_by('-units')[:5]
    return render(request,'dashboard/admin.html',{'revenue':revenue,'order_count':orders.count(),'customers':Profile.objects.filter(role='customer').count(),'products':Product.objects.count(),'sellers':Seller.objects.count(),'pending':orders.filter(status__in=['placed','confirmed']).count(),'low_stock':Product.objects.filter(stock__lte=5).count(),'top_products':top,'recent_orders':orders.select_related('user')[:8]})
@login_required
def seller_register(request):
    if hasattr(request.user,'seller_profile'): return redirect('dashboard:seller')
    form=SellerForm(request.POST or None)
    if request.method=='POST' and form.is_valid(): obj=form.save(commit=False); obj.user=request.user; obj.save(); profile,_=Profile.objects.get_or_create(user=request.user); profile.role='seller'; profile.save(); messages.success(request,'Seller profile created. You can add products now.'); return redirect('dashboard:seller')
    return render(request,'dashboard/seller_register.html',{'form':form})
@seller_required
def seller_dashboard(request):
    seller=request.user.seller_profile; products=seller.products.all(); items=OrderItem.objects.filter(product__seller=seller).exclude(order__status='cancelled'); revenue=items.aggregate(v=Sum(F('quantity')*F('price')))['v'] or 0
    return render(request,'dashboard/seller.html',{'seller':seller,'products':products,'orders':items.select_related('order','product')[:8],'revenue':revenue,'units':items.aggregate(v=Sum('quantity'))['v'] or 0})
@seller_required
def product_form(request,pk=None):
    seller=request.user.seller_profile; product=get_object_or_404(Product,pk=pk,seller=seller) if pk else None; form=ProductForm(request.POST or None,request.FILES or None,instance=product)
    if request.method=='POST' and form.is_valid(): obj=form.save(commit=False); obj.seller=seller; obj.save(); messages.success(request,'Product saved.'); return redirect('dashboard:seller')
    return render(request,'dashboard/product_form.html',{'form':form,'product':product})

@seller_required
def product_delete(request,pk):
    product=get_object_or_404(Product,pk=pk,seller=request.user.seller_profile)
    if request.method=='POST': product.delete(); messages.success(request,'Product deleted.')
    return redirect('dashboard:seller')
@seller_required
def product_delete(request,pk):
    product=get_object_or_404(Product,pk=pk,seller=request.user.seller_profile)
    if request.method=='POST': product.is_active=False; product.save(update_fields=['is_active']); messages.success(request,'Product archived.')
    return redirect('dashboard:seller')

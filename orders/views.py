from datetime import timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404,redirect,render
from django.utils import timezone
from accounts.forms import AddressForm
from accounts.models import Address
from store.cart import Cart
from .models import Order,OrderItem,Payment,ShippingAddress

@login_required
def checkout(request):
    cart=Cart(request)
    if not len(cart): messages.info(request,'Your cart is empty.'); return redirect('store:products')
    addresses=request.user.addresses.all()
    if request.method=='POST':
        address=get_object_or_404(Address,pk=request.POST.get('address_id'),user=request.user)
        payment_method=request.POST.get('payment_method','cod')
        if payment_method not in dict(Order.PAYMENT): payment_method='cod'
        with transaction.atomic():
            for item in cart.items():
                product=item['product']
                if item['quantity']>product.stock: messages.error(request,f'Only {product.stock} units of {product.name} remain.'); return redirect('store:cart')
            order=Order.objects.create(user=request.user,subtotal=cart.subtotal,discount=cart.discount,delivery_fee=cart.delivery,tax=cart.tax,total=cart.total,coupon=cart.coupon,payment_method=payment_method)
            ShippingAddress.objects.create(order=order,full_name=address.full_name,phone=address.phone,address=address.address,city=address.city,state=address.state,postal_code=address.postal_code,country=address.country)
            for item in cart.items():
                product=item['product']; OrderItem.objects.create(order=order,product=product,product_name=product.name,quantity=item['quantity'],price=product.price); product.stock-=item['quantity']; product.save(update_fields=['stock'])
            status='pending' if payment_method=='cod' else 'paid'; Payment.objects.create(order=order,provider='demo',transaction_id=f'DEMO-{order.number}',amount=order.total,status=status)
            if cart.coupon: cart.coupon.times_used+=1; cart.coupon.save(update_fields=['times_used'])
            cart.clear()
        return redirect('orders:success',number=order.number)
    return render(request,'orders/checkout.html',{'cart':cart,'addresses':addresses,'address_form':AddressForm()})

@login_required
def success(request,number):
    order=get_object_or_404(Order.objects.prefetch_related('items'),number=number,user=request.user)
    return render(request,'orders/success.html',{'order':order,'estimated':order.created_at+timedelta(days=5)})
@login_required
def order_list(request): return render(request,'orders/list.html',{'orders':request.user.orders.prefetch_related('items').order_by('-created_at')})
@login_required
def order_detail(request,number): return render(request,'orders/detail.html',{'order':get_object_or_404(Order.objects.prefetch_related('items__product'),number=number,user=request.user)})
@login_required
def track(request,number):
    order=get_object_or_404(Order,number=number,user=request.user); steps=['placed','confirmed','packed','shipped','out','delivered']; progress=(steps.index(order.status)+1)*100//len(steps) if order.status in steps else 0
    return render(request,'orders/track.html',{'order':order,'steps':steps,'progress':progress})
@login_required
def cancel(request,number):
    order=get_object_or_404(Order,number=number,user=request.user)
    if request.method=='POST' and order.status in ['placed','confirmed']:
        with transaction.atomic():
            for item in order.items.select_related('product'): item.product.stock+=item.quantity; item.product.save(update_fields=['stock'])
            order.status='cancelled'; order.save(update_fields=['status']); messages.success(request,'Order cancelled and stock restored.')
    else: messages.error(request,'This order can no longer be cancelled.')
    return redirect('orders:detail',number=number)

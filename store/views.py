from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q,Avg,Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404,redirect,render
from django.utils import timezone
from orders.models import OrderItem
from .cart import Cart
from .forms import ReviewForm
from .models import Brand,Category,Coupon,NewsletterSubscriber,Product,Review,Wishlist,WishlistItem

def home(request):
    products=Product.objects.filter(is_active=True).select_related('category','brand')
    return render(request,'store/home.html',{
        'featured':products.filter(is_featured=True)[:8],
        'best':products.filter(is_best_seller=True)[:8],
        'new':products.order_by('-created_at')[:8],
        'flash':products.filter(original_price__isnull=False).order_by('-original_price')[:8],
        'recommended':products.order_by('-rating','-is_featured')[:8],
        'categories':Category.objects.filter(is_active=True)[:10],
    })

def products(request):
    qs=Product.objects.filter(is_active=True).select_related('category','brand').annotate(review_count=Count('reviews'))
    q=request.GET.get('q','').strip(); category=request.GET.get('category'); brand=request.GET.get('brand')
    if q: qs=qs.filter(Q(name__icontains=q)|Q(brand__name__icontains=q)|Q(category__name__icontains=q))
    if category: qs=qs.filter(category__slug=category)
    if brand: qs=qs.filter(brand__slug=brand)
    for key,lookup in [('min_price','price__gte'),('max_price','price__lte'),('rating','rating__gte')]:
        if request.GET.get(key): qs=qs.filter(**{lookup:request.GET[key]})
    if request.GET.get('availability'): qs=qs.filter(stock__gt=0)
    sort={'price_asc':'price','price_desc':'-price','newest':'-created_at','rating':'-rating','discount':'price'}.get(request.GET.get('sort'),'-is_featured')
    qs=qs.order_by(sort)
    from django.core.paginator import Paginator
    page=Paginator(qs,12).get_page(request.GET.get('page'))
    return render(request,'store/products.html',{'page':page,'products':page.object_list,'categories':Category.objects.all(),'brands':Brand.objects.all(),'query':q})

def categories(request): return render(request,'store/categories.html',{'categories':Category.objects.annotate(product_count=Count('products'))})
def product_detail(request,slug):
    product=get_object_or_404(Product.objects.select_related('category','brand').prefetch_related('variants','images','reviews__user'),slug=slug,is_active=True)
    purchased=request.user.is_authenticated and OrderItem.objects.filter(order__user=request.user,order__status='delivered',product=product).exists()
    return render(request,'store/product_detail.html',{'product':product,'related':Product.objects.filter(category=product.category,is_active=True).exclude(pk=product.pk)[:4],'review_form':ReviewForm(),'purchased':purchased})

def cart_detail(request): return render(request,'store/cart.html',{'cart':Cart(request)})
def cart_add(request,pk):
    product=get_object_or_404(Product,pk=pk,is_active=True)
    if product.stock<1: messages.error(request,'This product is out of stock.')
    else: Cart(request).add(product,int(request.POST.get('quantity',1))); messages.success(request,f'{product.name} added to cart.')
    return JsonResponse({'ok':product.stock>0,'cart_count':len(Cart(request))}) if request.headers.get('X-Requested-With')=='XMLHttpRequest' else redirect(request.POST.get('next') or 'store:cart')
def cart_update(request,pk):
    product=get_object_or_404(Product,pk=pk); quantity=int(request.POST.get('quantity',1)); cart=Cart(request)
    if quantity<=0: cart.remove(product)
    else: cart.add(product,quantity,True)
    return redirect('store:cart')
def cart_remove(request,pk): Cart(request).remove(get_object_or_404(Product,pk=pk)); return redirect('store:cart')
def coupon_apply(request):
    coupon=Coupon.objects.filter(code__iexact=request.POST.get('code',''),is_active=True,start_date__lte=timezone.now(),expiry_date__gte=timezone.now()).first(); cart=Cart(request)
    if coupon and coupon.times_used<coupon.usage_limit and cart.subtotal>=coupon.minimum_order: request.session['coupon']=coupon.code; messages.success(request,f'{coupon.code} applied!')
    else: messages.error(request,'Coupon is invalid, expired, or minimum spend is not met.')
    return redirect('store:cart')
def coupon_remove(request): request.session.pop('coupon',None); return redirect('store:cart')

@login_required
def wishlist(request): return render(request,'store/wishlist.html',{'items':WishlistItem.objects.filter(wishlist__user=request.user).select_related('product')})
@login_required
def wishlist_toggle(request,pk):
    wish,_=Wishlist.objects.get_or_create(user=request.user); product=get_object_or_404(Product,pk=pk); item=WishlistItem.objects.filter(wishlist=wish,product=product).first()
    if item: item.delete(); active=False
    else: WishlistItem.objects.create(wishlist=wish,product=product); active=True
    return JsonResponse({'active':active,'count':wish.items.count()}) if request.headers.get('X-Requested-With')=='XMLHttpRequest' else redirect(request.POST.get('next') or 'store:wishlist')
@login_required
def wishlist_move(request,pk):
    item=get_object_or_404(WishlistItem,wishlist__user=request.user,product_id=pk); Cart(request).add(item.product); item.delete(); messages.success(request,'Moved to cart.'); return redirect('store:wishlist')
@login_required
def review_save(request,slug):
    product=get_object_or_404(Product,slug=slug); purchased=OrderItem.objects.filter(order__user=request.user,order__status='delivered',product=product).exists()
    if not purchased: messages.error(request,'Only verified buyers can review this product.'); return redirect(product)
    review=Review.objects.filter(user=request.user,product=product).first(); form=ReviewForm(request.POST,instance=review)
    if form.is_valid(): obj=form.save(commit=False); obj.user=request.user; obj.product=product; obj.save(); avg=product.reviews.aggregate(v=Avg('rating'))['v']; product.rating=avg; product.save(update_fields=['rating']); messages.success(request,'Thanks for your review!')
    else: messages.error(request,'Please correct the review form.')
    return redirect(product)
@login_required
def review_delete(request,pk):
    review=get_object_or_404(Review,pk=pk,user=request.user); product=review.product
    if request.method=='POST': review.delete(); product.rating=product.reviews.aggregate(v=Avg('rating'))['v'] or 0; product.save(update_fields=['rating'])
    return redirect(product)
def newsletter(request):
    if request.method=='POST': NewsletterSubscriber.objects.get_or_create(email=request.POST.get('email','')); messages.success(request,'You’re on the list!')
    return redirect('store:home')
def info_page(request,page): return render(request,f'store/{page}.html')
def custom_404(request,exception): return render(request,'404.html',status=404)

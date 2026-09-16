from .cart import Cart
from .models import Category,WishlistItem
def shopnest_context(request):
    wish=WishlistItem.objects.filter(wishlist__user=request.user).count() if request.user.is_authenticated else 0
    return {'nav_categories':Category.objects.filter(is_active=True)[:8],'cart_count':len(Cart(request)),'wishlist_count':wish}

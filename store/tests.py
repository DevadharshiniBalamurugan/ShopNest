from datetime import timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from accounts.models import Address,Profile
from orders.models import Order
from .models import Brand,Category,Coupon,Product,Seller

class CommerceFlowTests(TestCase):
    def setUp(self):
        self.user=User.objects.create_user('buyer','buyer@example.com','StrongPass123!')
        Profile.objects.create(user=self.user)
        self.address=Address.objects.create(user=self.user,full_name='Buyer One',phone='9999999999',address='1 Main Road',city='Chennai',state='Tamil Nadu',postal_code='600001',country='India',is_default=True)
        category=Category.objects.create(name='Electronics',slug='electronics')
        brand=Brand.objects.create(name='Nova',slug='nova')
        self.product=Product.objects.create(name='Test Headphones',slug='test-headphones',description='Excellent.',price=1000,original_price=1200,category=category,brand=brand,sku='TEST-1',stock=5,is_active=True)
        Coupon.objects.create(code='TEST10',discount_type='percent',discount_value=10,minimum_order=500,start_date=timezone.now()-timedelta(days=1),expiry_date=timezone.now()+timedelta(days=1))
    def test_public_catalog_and_search(self):
        self.assertEqual(self.client.get(reverse('store:home')).status_code,200)
        response=self.client.get(reverse('store:products'),{'q':'Headphones'})
        self.assertContains(response,'Test Headphones')
    def test_registration_hashes_password(self):
        response=self.client.post(reverse('accounts:register'),{'first_name':'New','last_name':'User','username':'newuser','email':'new@example.com','role':'customer','password1':'UniquePass985!','password2':'UniquePass985!'})
        self.assertEqual(response.status_code,302); self.assertTrue(User.objects.get(username='newuser').check_password('UniquePass985!'))
    def test_cart_coupon_wishlist_checkout(self):
        self.client.force_login(self.user)
        self.client.post(reverse('store:cart_add',args=[self.product.pk]),{'quantity':2})
        self.client.post(reverse('store:coupon_apply'),{'code':'TEST10'})
        cart=self.client.get(reverse('store:cart')); self.assertContains(cart,'₹2000.00'); self.assertContains(cart,'TEST10')
        self.client.post(reverse('store:wishlist_toggle',args=[self.product.pk])); self.assertContains(self.client.get(reverse('store:wishlist')),'Test Headphones')
        result=self.client.post(reverse('orders:checkout'),{'address_id':self.address.pk,'payment_method':'card'})
        self.assertEqual(result.status_code,302); order=Order.objects.get(); self.assertEqual(order.items.count(),1); self.assertEqual(order.payment.status,'paid')
    def test_permissions_and_seller_ownership(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse('dashboard:admin')).status_code,302)
        self.assertRedirects(self.client.get(reverse('dashboard:seller')),reverse('dashboard:seller_register'))
    def test_all_customer_templates_render(self):
        public=['store:home','store:products','store:categories','store:about','store:contact','store:privacy','store:terms','accounts:login','accounts:register','accounts:password_reset']
        for name in public:
            with self.subTest(name=name): self.assertEqual(self.client.get(reverse(name)).status_code,200)
        self.client.force_login(self.user)
        self.client.post(reverse('store:cart_add',args=[self.product.pk]),{'quantity':1})
        authenticated=['accounts:profile','accounts:edit_profile','accounts:addresses','accounts:address_add','store:cart','store:wishlist','orders:list','orders:checkout']
        for name in authenticated:
            with self.subTest(name=name): self.assertEqual(self.client.get(reverse(name)).status_code,200)
        self.assertEqual(self.client.get(self.product.get_absolute_url()).status_code,200)
        self.client.post(reverse('orders:checkout'),{'address_id':self.address.pk,'payment_method':'cod'})
        order=Order.objects.get()
        self.assertEqual(self.client.get(reverse('orders:detail',args=[order.number])).status_code,200)
        self.assertEqual(self.client.get(reverse('orders:track',args=[order.number])).status_code,200)
    def test_seller_and_admin_dashboards_render(self):
        seller_user=User.objects.create_user('seller','seller@example.com','StrongPass123!')
        Profile.objects.create(user=seller_user,role='seller'); Seller.objects.create(user=seller_user,store_name='Test Store',approved=True)
        self.client.force_login(seller_user)
        self.assertEqual(self.client.get(reverse('dashboard:seller')).status_code,200)
        self.assertEqual(self.client.get(reverse('dashboard:product_add')).status_code,200)
        admin=User.objects.create_superuser('staff','staff@example.com','StrongPass123!')
        Profile.objects.create(user=admin); self.client.force_login(admin)
        self.assertEqual(self.client.get(reverse('dashboard:admin')).status_code,200)

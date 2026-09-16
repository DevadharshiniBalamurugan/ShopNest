from datetime import timedelta
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from accounts.models import Profile,Address
from store.models import Brand,Category,Coupon,Product,Seller,ProductVariant

PRODUCTS=[
('Nova Wireless Headphones','Electronics','Nova','3299','4999','A calm, immersive listening experience with active noise reduction and an ultra-comfortable fit.','https://images.unsplash.com/photo-1576082712237-eb1335ce23a3?auto=format&fit=crop&w=900&q=80',4.8,24),
('Pulse S2 Smart Watch','Electronics','Pulse','4499','6499','Track workouts, sleep, heart rate, and everyday progress in a beautifully minimal watch.','/static/images/products/pulse-s2-smart-watch.webp',4.7,18),
('Drift Bluetooth Speaker','Electronics','Drift','2199','2999','Room-filling portable sound with a tactile fabric finish and all-day battery.','https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=900&q=80',4.6,16),
('Typecraft Mechanical Keyboard','Electronics','Typecraft','3799','4999','Crisp tactile switches, warm backlighting, and a compact desk-friendly layout.','https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=900&q=80',4.9,12),
('Everyday Cotton Tee','Men’s Clothing','Threadline','799','1199','A breathable heavyweight cotton t-shirt cut for an easy modern fit.','https://images.unsplash.com/photo-1581655353564-df123a1eb820?auto=format&fit=crop&w=900&q=80',4.5,40),
('Cloudstep Sneakers','Shoes','Cloudstep','2899','4299','Lightweight knit sneakers with cushioned support for days that keep moving.','https://images.unsplash.com/photo-1669671943625-e20799ee5f42?auto=format&fit=crop&w=900&q=80',4.8,22),
('Indigo Denim Jacket','Fashion','Threadline','2599','3599','A versatile mid-weight denim layer with clean hardware and a lived-in finish.','https://images.unsplash.com/photo-1543076447-215ad9ba6923?auto=format&fit=crop&w=900&q=80',4.6,14),
('Softform Essential Hoodie','Women’s Clothing','Softform','1899','2799','Brushed cotton comfort in a relaxed silhouette, designed for repeat wear.','https://images.unsplash.com/photo-1620799140188-3b2a02fd9a77?auto=format&fit=crop&w=900&q=80',4.7,28),
('Halo Table Lamp','Home & Kitchen','Halo Home','1699','2299','Warm, dimmable light in a sculptural silhouette for desks and bedside tables.','https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=900&q=80',4.7,11),
('Brewmate Coffee Maker','Home & Kitchen','Brewmate','3499','4699','A compact coffee maker for balanced, aromatic cups without the counter clutter.','https://images.unsplash.com/photo-1707241358597-bafcc8a8e73d?auto=format&fit=crop&w=900&q=80',4.5,9),
('Clearspace Organizer Set','Home & Kitchen','Clearspace','999','1499','Modular, stackable organizers that make everyday storage feel effortless.','https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=900&q=80',4.4,35),
('Kind Skin Face Wash','Beauty','Kind Skin','499','699','A gentle daily cleanser with a soft lather that leaves skin comfortable.','https://images.unsplash.com/photo-1653919198052-546d44e2458e?auto=format&fit=crop&w=900&q=80',4.6,50),
('Dewdrop Moisturizer','Beauty','Dewdrop','849','1199','Weightless, lasting hydration with a fresh, non-greasy finish.','https://images.unsplash.com/photo-1556229010-6c3f2c9ca5f8?auto=format&fit=crop&w=900&q=80',4.8,33),
('No. 08 Eau de Parfum','Beauty','Atelier Eight','1999','2799','A modern blend of bergamot, soft woods, and warm amber.','https://images.unsplash.com/photo-1666621630026-862eea07236c?auto=format&fit=crop&w=900&q=80',4.7,15),
('Motion Yoga Mat','Sports','Motion','1299','1799','Grippy, supportive cushioning for stretching, strength, and daily practice.','https://images.unsplash.com/photo-1646239646963-b0b9be56d6b5?auto=format&fit=crop&w=900&q=80',4.5,20),
('Metro Crossbody Bag','Accessories','Modo','1499','2199','A compact everyday carry with considered pockets and an adjustable strap.','https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=900&q=80',4.6,17),
('Morning Grove Granola','Grocery','Morning Grove','599','799','Crunchy whole-grain clusters with almonds, pumpkin seeds, and naturally sweet dried berries.','https://images.unsplash.com/photo-1725883691833-97103ecd582a?auto=format&fit=crop&w=900&q=80',4.8,42),
('Flex 24 Adjustable Dumbbells','Sports','Motion','6999','8999','A compact adjustable dumbbell pair for progressive home strength training without equipment clutter.','/static/images/products/flex-adjustable-dumbbells.webp',4.9,14),
('Solace Polarized Sunglasses','Accessories','Modo','1299','1899','Lightweight polarized sunglasses with warm amber lenses, UV protection, and a protective case.','https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?auto=format&fit=crop&w=900&q=80',4.7,31),
]
class Command(BaseCommand):
    help='Create realistic ShopNest demo data and accounts'
    def handle(self,*args,**kwargs):
        cats={'Electronics':'⌁','Fashion':'✦','Men’s Clothing':'◈','Women’s Clothing':'◇','Shoes':'◒','Beauty':'❀','Home & Kitchen':'⌂','Accessories':'◉','Grocery':'♧','Sports':'⚡'}
        for name,icon in cats.items(): Category.objects.update_or_create(slug=slugify(name),defaults={'name':name,'icon':icon,'description':f'Discover smart {name.lower()} picks.'})
        brands={}
        for row in PRODUCTS: brands[row[2]]=Brand.objects.get_or_create(name=row[2],slug=slugify(row[2]))[0]
        seller_user,_=User.objects.get_or_create(username='seller_demo',defaults={'email':'seller@shopnest.demo','first_name':'Sam'}); seller_user.set_password('Seller@123'); seller_user.save(); Profile.objects.update_or_create(user=seller_user,defaults={'role':'seller'}); seller,_=Seller.objects.update_or_create(user=seller_user,defaults={'store_name':'ShopNest Select','approved':True})
        for i,(name,cat,brand,price,original,desc,image,rating,stock) in enumerate(PRODUCTS):
            p,_=Product.objects.update_or_create(slug=slugify(name),defaults={'name':name,'description':desc,'price':Decimal(price),'original_price':Decimal(original),'category':Category.objects.get(name=cat),'brand':brands[brand],'seller':seller,'sku':f'CTV-{i+1:04}','stock':stock,'main_image':image,'rating':rating,'is_active':True,'is_featured':i<8,'is_best_seller':i in [0,1,5,8,12,15],'specifications':{'Warranty':'1 year','Country of origin':'India','Return window':'7 days'}})
            if i in [4,5,7]:
                for value in ['S','M','L','XL']: ProductVariant.objects.get_or_create(product=p,name='Size',value=value,defaults={'stock':8})
        now=timezone.now()
        for code,typ,value,minv,maxv in [('SHOPNEST10','percent',10,999,500),('WELCOME20','percent',20,1499,800),('SAVE15','percent',15,1999,600)]: Coupon.objects.update_or_create(code=code,defaults={'discount_type':typ,'discount_value':value,'minimum_order':minv,'maximum_discount':maxv,'start_date':now-timedelta(days=1),'expiry_date':now+timedelta(days=365),'usage_limit':1000,'is_active':True})
        admin,_=User.objects.get_or_create(username='admin',defaults={'email':'admin@shopnest.demo','is_staff':True,'is_superuser':True}); admin.is_staff=True; admin.is_superuser=True; admin.set_password('Admin@123'); admin.save(); Profile.objects.get_or_create(user=admin)
        customer,_=User.objects.get_or_create(username='customer_demo',defaults={'email':'customer@shopnest.demo','first_name':'Maya'}); customer.set_password('Customer@123'); customer.save(); Profile.objects.get_or_create(user=customer); Address.objects.get_or_create(user=customer,address='42 Lake View Road',defaults={'full_name':'Maya Rao','phone':'9876543210','city':'Bengaluru','state':'Karnataka','postal_code':'560001','country':'India','is_default':True})
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(PRODUCTS)} products and demo accounts.'))

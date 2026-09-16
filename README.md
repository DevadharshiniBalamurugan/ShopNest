# ShopNest

**Shop Smart. Live Better.**

ShopNest is a production-style, responsive e-commerce portfolio project built with Django templates, Tailwind CSS, and vanilla JavaScript. It includes a polished customer storefront, secure authentication, session cart, database wishlist, multi-step checkout, order tracking, reviews, seller tools, and a custom business dashboard.

## Highlights

- Responsive home, catalog, category, search, filter, product, cart, wishlist, and checkout pages
- Django authentication with registration, login/logout, password reset, profiles, and addresses
- Server-validated coupons, stock control, simulated COD/card/UPI payments, and transactional order creation
- Order history, details, progress tracking, eligible cancellation, and inventory restoration
- Verified-purchase product reviews with aggregate ratings
- Customer, seller, and staff roles with server-side authorization checks
- Seller-owned product management and sales summary
- Staff-only revenue, order, customer, inventory, and top-product dashboard
- CSRF protection, ORM queries, password hashing, upload handling, validation, and environment-based secrets
- Original AI-generated hero artwork stored locally; product seed photos use remote Unsplash demo URLs

## Tech stack

- Python 3 and Django 6
- SQLite by default; MySQL-ready environment configuration
- Django ORM and Django Templates
- Tailwind CSS via CDN plus a small project design-system stylesheet
- Vanilla JavaScript for menus, toasts, cart/wishlist AJAX, quick view, galleries, and quantity controls

## Project layout

```text
shopnest/       Project settings and root URLs
accounts/      Profiles, roles, authentication, addresses
store/         Catalog, search, cart, wishlist, coupons, reviews, seed command
orders/        Checkout, order items, payment, tracking
dashboard/     Seller and custom staff dashboards
templates/     Responsive Django templates
static/        CSS, JavaScript, and original hero art
media/         User and product uploads
```

## Local setup

1. Create and activate a virtual environment.

   Windows PowerShell:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   macOS/Linux:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies.

   ```bash
   pip install -r requirements.txt
   ```

   If you only need SQLite and your machine lacks MySQL build tools, install `Django`, `Pillow`, and `python-dotenv` directly; `mysqlclient` is only needed for MySQL.

3. Copy `.env.example` to `.env` and set a strong `DJANGO_SECRET_KEY` for deployed environments. Environment variables can be exported by your process manager; the settings module reads them directly.

4. Create the database and demo content.

   ```bash
   python manage.py migrate
   python manage.py seed_data
   ```

5. Start the site.

   ```bash
   python manage.py runserver
   ```

   Visit `http://127.0.0.1:8000/`.

   ## Deployment

   The SQLite database and `media/` uploads are intentionally ignored by Git. A fresh deployment therefore needs to create its database and seed the catalog during the build. Configure these environment variables on the host:

   ```dotenv
   DJANGO_SECRET_KEY=use-a-long-random-value
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=your-domain.example
   DJANGO_CSRF_TRUSTED_ORIGINS=https://your-domain.example
   ```

   Use this as the deployment build command:

   ```bash
   python manage.py migrate --noinput && python manage.py seed_data && python manage.py collectstatic --noinput
   ```

   Start the web process with:

   ```bash
   gunicorn shopnest.wsgi:application
   ```

   Run the build command again whenever the deployment uses a new empty database. For uploaded product images, configure persistent media storage or copy the `media/` directory to the host; the catalog images included with the demo data are stored in `static/images/products/` and are collected by the build command.

## MySQL configuration

Create a UTF-8 MySQL database, then set:

```dotenv
DB_ENGINE=mysql
DB_NAME=shopnest
DB_USER=shopnest
DB_PASSWORD=your-password
DB_HOST=127.0.0.1
DB_PORT=3306
```

Run `python manage.py migrate` after switching databases.

## Demo credentials

| Role | Username | Password | Entry point |
|---|---|---|---|
| Customer | `customer_demo` | `Customer@123` | `/account/login/` |
| Seller | `seller_demo` | `Seller@123` | `/dashboard/seller/` |
| Admin | `admin` | `Admin@123` | `/dashboard/admin/` |

The advanced Django admin is available at `/django-admin/`. Change every demo password before any public deployment.

Demo coupon codes: `SHOPNEST10`, `WELCOME20`, and `SAVE15`.

## Testing

```bash
python manage.py check
python manage.py test
```

The included integration tests cover catalog/search, password hashing during registration, cart/coupon/wishlist/checkout, payment creation, and role restrictions.

## Screenshots

Add final screenshots here after running the application locally:

- Homepage (desktop and mobile)
- Product catalog and detail
- Checkout and confirmation
- Seller dashboard
- Admin dashboard

## Production notes and future improvements

This repository deliberately uses safe simulated online payments and console email. Before production, integrate a real payment provider through its server SDK, transactional email, object storage/CDN for uploads, a compiled Tailwind build, background jobs for notifications, rate limiting, and a complete returns/refunds workflow. Configure HTTPS, secure cookies, trusted origins, production logging, and managed MySQL credentials in the deployment environment.

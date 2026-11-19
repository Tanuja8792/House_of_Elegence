# House of Elegance

A Django-powered fashion e-commerce demo inspired by modern fashion marketplaces.

## Features
- Responsive fashion storefront with category filtering and product search
- Database-backed product catalogue with descriptions, image URLs, prices and automatic discount percentages
- Session-based shopping cart with quantity updates and item removal
- Checkout form with delivery address collection
- Cash on Delivery demo order placement and order confirmation
- Order history lookup by checkout email
- Django admin management for products and orders

## Run locally (Windows CMD)

1. Clone or download this repository and open the folder containing `manage.py`.
2. Create and activate a virtual environment:
   ```cmd
   py -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```
4. Apply migrations and start the server:
   ```cmd
   python manage.py migrate
   python manage.py runserver
   ```
5. Visit http://127.0.0.1:8000/.

The first homepage visit seeds 12 sample fashion products into the database. Product records can be edited in Django admin after creating an admin account with `python manage.py createsuperuser`; open http://127.0.0.1:8000/admin/.

## Shopping flow
Browse products → Add to Bag → Update quantities → Proceed to Checkout → Enter delivery details → Place Order → View confirmation.

Use the My Orders link and enter the same email used at checkout to find demo orders.

## Important payment note
Checkout currently supports **Cash on Delivery as a demonstration only**. It stores orders in the local database; it does not collect money, connect to a bank, or process live online payments. A real payment provider (such as Razorpay) requires a merchant account and server-side API keys before production use.

## Project structure
- `config/` — Django project configuration
- `store/models.py` — Product, Order and OrderItem database models
- `store/views.py` — catalogue, cart, checkout and order views
- `store/migrations/` — database schema migration
- `templates/` — storefront and shopping pages
- `static/css/` and `static/js/` — styling and small UI interactions

This is a learning/demo project. Before public deployment, configure a secure environment-based SECRET_KEY, DEBUG=False, production ALLOWED_HOSTS, HTTPS, email verification, privacy protections and a real payment integration.

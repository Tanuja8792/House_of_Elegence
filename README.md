# House of Elegance

A responsive women's fashion storefront built with HTML, CSS and JavaScript, integrated with Django for local development.

## Features
- Fashion homepage and seasonal hero section
- Women's categories: Ethnic Wear, Western Wear, Dresses, Tops, Footwear and Accessories
- Product cards with prices and discounts
- Category filtering and product search
- Wishlist and shopping-bag demo interactions
- Responsive desktop and mobile layout

## Run locally with Django

1. Open a terminal in the project folder.
2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   ```

   Windows CMD:

   ```cmd
   venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

5. Start the development server:

   ```bash
   python manage.py runserver
   ```

6. Open http://127.0.0.1:8000/ in your browser.

## Project layout

- `config/` — Django project settings and URL configuration
- `store/` — Django homepage app
- `templates/index.html` — Django-rendered storefront
- `static/css/style.css` — website styling
- `static/js/script.js` — product filtering and demo interactions

The current shopping bag, wishlist and newsletter are front-end demonstrations. There is no database-backed product catalogue, customer account, payment gateway or order processing yet.

## Note

The Django development server is for local development only. Set a secure environment-based secret key, configure allowed hosts, and use production settings before deployment.

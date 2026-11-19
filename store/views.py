from decimal import Decimal
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from .models import Order, OrderItem, Product

DEMO_PRODUCTS = [
("Floral Printed Kurta Set","Ethnic Wear","A comfortable printed kurta set for festive days and everyday elegance.","https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=800&q=85",1899,2499),
("Everyday Chic Midi Dress","Dresses","A versatile midi dress for day-to-evening styling.","https://images.unsplash.com/photo-1496747611176-843222e1e57c?auto=format&fit=crop&w=800&q=85",1599,2199),
("Classic White Summer Top","Tops","A light wardrobe essential for warm-weather looks.","https://images.unsplash.com/photo-1489602642804-64eda9c6c8ca?auto=format&fit=crop&w=800&q=85",899,1299),
("Elegant Occasion Saree","Ethnic Wear","An occasion-ready saree for celebrations.","https://images.unsplash.com/photo-1583391733956-6c78276477e5?auto=format&fit=crop&w=800&q=85",2799,3499),
("Modern Streetwear Co-ord","Western Wear","A coordinated contemporary outfit.","https://images.unsplash.com/photo-1539109136881-3be0616acf4b?auto=format&fit=crop&w=800&q=85",1999,2699),
("Soft Pastel Anarkali","Ethnic Wear","A graceful pastel outfit for special occasions.","https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?auto=format&fit=crop&w=800&q=85",2299,2999),
("Minimal Gold-Tone Earrings","Accessories","Minimal earrings for everyday and occasion wear.","https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?auto=format&fit=crop&w=800&q=85",499,799),
("Everyday Comfort Sneakers","Footwear","Comfort-first sneakers for all-day wear.","https://images.unsplash.com/photo-1543163521-1bf539c55dd2?auto=format&fit=crop&w=800&q=85",1499,1999),
("Elegant Black Evening Dress","Dresses","A timeless black dress for parties and celebrations.","https://images.unsplash.com/photo-1566174053879-31528523f8ae?auto=format&fit=crop&w=800&q=85",2199,2899),
("Relaxed Fit Linen Shirt","Tops","A relaxed shirt for smart-casual styling.","https://images.unsplash.com/photo-1551163943-3f6a855d1153?auto=format&fit=crop&w=800&q=85",1099,1499),
("Statement Heeled Sandals","Footwear","Statement heels for festive and evening outfits.","https://images.unsplash.com/photo-1515347619252-60a4bf4fff4f?auto=format&fit=crop&w=800&q=85",1699,2299),
("Everyday Shoulder Bag","Accessories","A versatile shoulder bag for daily essentials.","https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=800&q=85",1299,1799),
]

def seed_demo_products():
    if not Product.objects.exists():
        for name, category, description, image, price, old_price in DEMO_PRODUCTS:
            Product.objects.create(name=name, category=category, description=description, image_url=image, price=Decimal(str(price)), original_price=Decimal(str(old_price)))

def cart_details(request):
    cart=request.session.get("cart",{}); items=[]; total=Decimal("0.00"); count=0
    for pid, qty in cart.items():
        product=Product.objects.filter(pk=pid,is_active=True).first()
        if product and int(qty)>0:
            subtotal=product.price*int(qty); items.append({"product":product,"quantity":int(qty),"subtotal":subtotal}); total+=subtotal; count+=int(qty)
    return items,total,count

def home(request):
    seed_demo_products()
    products=Product.objects.filter(is_active=True).order_by("-created_at")
    category=request.GET.get("category",""); search=request.GET.get("q","").strip()
    if category: products=products.filter(category=category)
    if search: products=products.filter(name__icontains=search)
    _,_,count=cart_details(request)
    return render(request,"index.html",{"products":products,"categories":Product.CATEGORY_CHOICES,"active_category":category,"search_query":search,"cart_count":count})

def add_to_cart(request,product_id):
    if request.method!="POST": return redirect("home")
    product=get_object_or_404(Product,pk=product_id,is_active=True); cart=request.session.get("cart",{}); key=str(product.pk)
    cart[key]=min(int(cart.get(key,0))+1,20); request.session["cart"]=cart
    messages.success(request,f"{product.name} added to your bag.")
    return redirect(request.META.get("HTTP_REFERER","home"))

def cart_view(request):
    items,total,count=cart_details(request)
    return render(request,"store/cart.html",{"items":items,"total":total,"cart_count":count})

def update_cart(request,product_id):
    if request.method=="POST":
        cart=request.session.get("cart",{}); key=str(product_id); qty=int(request.POST.get("quantity",1))
        if qty<=0: cart.pop(key,None)
        elif key in cart: cart[key]=min(qty,20)
        request.session["cart"]=cart
    return redirect("cart")

def remove_from_cart(request,product_id):
    if request.method=="POST":
        cart=request.session.get("cart",{}); cart.pop(str(product_id),None); request.session["cart"]=cart
    return redirect("cart")

def checkout(request):
    items,total,count=cart_details(request)
    if not items:
        messages.info(request,"Your bag is empty."); return redirect("home")
    if request.method=="POST":
        fields=["customer_name","email","phone","address","city","state","pincode"]
        if any(not request.POST.get(f,"").strip() for f in fields):
            messages.error(request,"Please complete all delivery details.")
            return render(request,"store/checkout.html",{"items":items,"total":total,"cart_count":count})
        with transaction.atomic():
            order=Order.objects.create(customer_name=request.POST["customer_name"].strip(),email=request.POST["email"].strip(),phone=request.POST["phone"].strip(),address=request.POST["address"].strip(),city=request.POST["city"].strip(),state=request.POST["state"].strip(),pincode=request.POST["pincode"].strip(),total_amount=total)
            for item in items:
                OrderItem.objects.create(order=order,product=item["product"],product_name=item["product"].name,unit_price=item["product"].price,quantity=item["quantity"])
        request.session["cart"]={}; return redirect("order_success",order_id=order.pk)
    return render(request,"store/checkout.html",{"items":items,"total":total,"cart_count":count})

def order_success(request,order_id):
    order=get_object_or_404(Order,pk=order_id)
    return render(request,"store/order_success.html",{"order":order})

def my_orders(request):
    email=request.GET.get("email","").strip()
    order_id=request.GET.get("order_id","").strip()
    orders=Order.objects.none()
    if email and order_id.isdigit():
        orders=Order.objects.filter(email__iexact=email,pk=int(order_id)).order_by("-created_at")
    return render(request,"store/my_orders.html",{"orders":orders,"email":email,"order_id":order_id})

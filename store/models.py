from django.db import models
from decimal import Decimal

class Product(models.Model):
    CATEGORY_CHOICES = [("Ethnic Wear","Ethnic Wear"),("Western Wear","Western Wear"),("Dresses","Dresses"),("Tops","Tops"),("Footwear","Footwear"),("Accessories","Accessories")]
    name = models.CharField(max_length=180)
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES)
    description = models.TextField()
    image_url = models.URLField(max_length=600)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def discount_percent(self):
        if self.original_price <= self.price: return 0
        return round((1 - self.price / self.original_price) * 100)
    def __str__(self): return self.name

class Order(models.Model):
    STATUS_CHOICES = [(s,s) for s in ["Placed","Processing","Shipped","Delivered","Cancelled"]]
    customer_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=80)
    pincode = models.CharField(max_length=10)
    payment_method = models.CharField(max_length=30, default="Cash on Delivery")
    payment_status = models.CharField(max_length=30, default="Pending")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Placed")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"Order #{self.pk} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=180)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    @property
    def subtotal(self): return self.unit_price * self.quantity

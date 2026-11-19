from django.db import migrations, models
import django.db.models.deletion
from decimal import Decimal

class Migration(migrations.Migration):
    initial=True
    dependencies=[]
    operations=[
      migrations.CreateModel(name="Product",fields=[
        ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
        ("name",models.CharField(max_length=180)),("category",models.CharField(choices=[("Ethnic Wear","Ethnic Wear"),("Western Wear","Western Wear"),("Dresses","Dresses"),("Tops","Tops"),("Footwear","Footwear"),("Accessories","Accessories")],max_length=40)),
        ("description",models.TextField()),("image_url",models.URLField(max_length=600)),("price",models.DecimalField(decimal_places=2,max_digits=10)),("original_price",models.DecimalField(decimal_places=2,max_digits=10)),("is_active",models.BooleanField(default=True)),("created_at",models.DateTimeField(auto_now_add=True))]),
      migrations.CreateModel(name="Order",fields=[
        ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("customer_name",models.CharField(max_length=120)),("email",models.EmailField(max_length=254)),("phone",models.CharField(max_length=20)),("address",models.TextField()),("city",models.CharField(max_length=80)),("state",models.CharField(max_length=80)),("pincode",models.CharField(max_length=10)),("payment_method",models.CharField(default="Cash on Delivery",max_length=30)),("payment_status",models.CharField(default="Pending",max_length=30)),("status",models.CharField(choices=[("Placed","Placed"),("Processing","Processing"),("Shipped","Shipped"),("Delivered","Delivered"),("Cancelled","Cancelled")],default="Placed",max_length=20)),("total_amount",models.DecimalField(decimal_places=2,default=Decimal("0.00"),max_digits=10)),("created_at",models.DateTimeField(auto_now_add=True))]),
      migrations.CreateModel(name="OrderItem",fields=[
        ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("product_name",models.CharField(max_length=180)),("unit_price",models.DecimalField(decimal_places=2,max_digits=10)),("quantity",models.PositiveIntegerField(default=1)),("order",models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name="items",to="store.order")),("product",models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,to="store.product"))])
    ]
from django.contrib import admin
from .models import Order, OrderItem, Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=("name","category","price","original_price","is_active")
    list_filter=("category","is_active")
    search_fields=("name","description")

class OrderItemInline(admin.TabularInline):
    model=OrderItem
    extra=0
    readonly_fields=("product","product_name","unit_price","quantity")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=("id","customer_name","email","total_amount","status","payment_status","created_at")
    list_filter=("status","payment_status","created_at")
    search_fields=("customer_name","email","phone")
    inlines=[OrderItemInline]

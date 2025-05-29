from django.contrib import admin
from .models import Category, Product, Customer, Sale, SaleItem, Expense

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'size', 'color', 'price', 'stock_quantity', 'sku']
    list_filter = ['category', 'size', 'color']
    search_fields = ['name', 'sku']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at']
    search_fields = ['name', 'email', 'phone']

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'total_amount', 'payment_method', 'sale_date']
    list_filter = ['payment_method', 'sale_date']
    inlines = [SaleItemInline]

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['description', 'amount', 'expense_type', 'date']
    list_filter = ['expense_type', 'date']
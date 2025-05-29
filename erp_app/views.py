from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Product, Category, Customer, Sale, SaleItem, Expense
import json


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    # Calculate financial metrics
    today = timezone.now().date()
    this_month = today.replace(day=1)

    # Sales data
    total_sales = Sale.objects.filter(sale_date__gte=this_month).aggregate(
        total=Sum('total_amount'))['total'] or 0

    # Expenses data
    total_expenses = Expense.objects.filter(date__gte=this_month).aggregate(
        total=Sum('amount'))['total'] or 0

    # Investment (stock value)
    total_investment = Product.objects.aggregate(
        total=Sum('cost_price'))['total'] or 0

    # Recent transactions
    recent_sales = Sale.objects.order_by('-sale_date')[:5]

    # Chart data for distributions
    sales_by_category = []
    categories = Category.objects.all()
    for category in categories:
        category_sales = SaleItem.objects.filter(
            product__category=category,
            sale__sale_date__gte=this_month
        ).aggregate(total=Sum('total_price'))['total'] or 0
        sales_by_category.append({
            'name': category.name,
            'value': float(category_sales)
        })

    context = {
        'total_savings': total_sales - total_expenses,
        'total_expenses': total_expenses,
        'total_investment': total_investment,
        'recent_sales': recent_sales,
        'sales_by_category': json.dumps(sales_by_category),
    }
    return render(request, 'dashboard.html', context)


@login_required
def products(request):
    products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all()

    if request.method == 'POST':
        # Add new product
        name = request.POST['name']
        category_id = request.POST['category']
        size = request.POST['size']
        color = request.POST['color']
        price = request.POST['price']
        cost_price = request.POST['cost_price']
        stock_quantity = request.POST['stock_quantity']
        sku = request.POST['sku']
        description = request.POST.get('description', '')

        category = get_object_or_404(Category, id=category_id)

        Product.objects.create(
            name=name,
            category=category,
            size=size,
            color=color,
            price=price,
            cost_price=cost_price,
            stock_quantity=stock_quantity,
            sku=sku,
            description=description
        )
        messages.success(request, 'Product added successfully!')
        return redirect('products')

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'products.html', context)


@login_required
def customers(request):
    customers = Customer.objects.all().order_by('-created_at')

    if request.method == 'POST':
        # Add new customer
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']

        Customer.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address
        )
        messages.success(request, 'Customer added successfully!')
        return redirect('customers')

    context = {
        'customers': customers,
    }
    return render(request, 'customers.html', context)


@login_required
def sales(request):
    sales = Sale.objects.all().order_by('-sale_date')
    customers = Customer.objects.all()
    products = Product.objects.filter(stock_quantity__gt=0)

    if request.method == 'POST':
        # Add new sale
        customer_id = request.POST['customer']
        payment_method = request.POST['payment_method']
        notes = request.POST.get('notes', '')

        customer = get_object_or_404(Customer, id=customer_id)

        # Create sale
        sale = Sale.objects.create(
            customer=customer,
            total_amount=0,  # Will be updated after adding items
            payment_method=payment_method,
            notes=notes,
            created_by=request.user
        )

        # Add sale items (simplified - in real app, this would be more complex)
        total_amount = 0
        product_ids = request.POST.getlist('products')
        quantities = request.POST.getlist('quantities')

        for i, product_id in enumerate(product_ids):
            if product_id and i < len(quantities):
                product = get_object_or_404(Product, id=product_id)
                quantity = int(quantities[i])

                SaleItem.objects.create(
                    sale=sale,
                    product=product,
                    quantity=quantity,
                    unit_price=product.price,
                    total_price=quantity * product.price
                )

                # Update stock
                product.stock_quantity -= quantity
                product.save()

                total_amount += quantity * product.price

        # Update sale total
        sale.total_amount = total_amount
        sale.save()

        messages.success(request, 'Sale recorded successfully!')
        return redirect('sales')

    context = {
        'sales': sales,
        'customers': customers,
        'products': products,
    }
    return render(request, 'sales.html', context)


@login_required
def reports(request):
    # Generate various reports
    today = timezone.now().date()
    this_month = today.replace(day=1)

    # Monthly sales report
    monthly_sales = Sale.objects.filter(sale_date__gte=this_month).aggregate(
        total_sales=Sum('total_amount'),
        total_orders=Count('id')
    )

    # Top selling products
    top_products = SaleItem.objects.filter(
        sale__sale_date__gte=this_month
    ).values('product__name').annotate(
        total_sold=Sum('quantity'),
        total_revenue=Sum('total_price')
    ).order_by('-total_sold')[:10]

    # Low stock products
    low_stock_products = Product.objects.filter(stock_quantity__lt=10)

    context = {
        'monthly_sales': monthly_sales,
        'top_products': top_products,
        'low_stock_products': low_stock_products,
    }
    return render(request, 'reports.html', context)
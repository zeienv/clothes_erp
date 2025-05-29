from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from erp_app.models import Category, Product, Customer, Sale, SaleItem, Expense
from django.utils import timezone
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Populate the database with dummy data for clothes shop'

    def handle(self, *args, **options):
        self.stdout.write('Creating dummy data...')

        # Create superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write('Created admin user (username: admin, password: admin123)')

        # Create categories
        categories_data = [
            {'name': 'T-Shirts', 'description': 'Casual and formal t-shirts'},
            {'name': 'Jeans', 'description': 'Denim jeans for all occasions'},
            {'name': 'Dresses', 'description': 'Elegant dresses for women'},
            {'name': 'Jackets', 'description': 'Warm and stylish jackets'},
            {'name': 'Shoes', 'description': 'Footwear collection'},
            {'name': 'Accessories', 'description': 'Bags, belts, and accessories'},
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create products
        products_data = [
            # T-Shirts
            {'name': 'Cotton Basic T-Shirt', 'category': 'T-Shirts', 'sizes': ['S', 'M', 'L', 'XL'],
             'colors': ['White', 'Black', 'Navy', 'Gray'], 'price': 25.99, 'cost': 12.50},
            {'name': 'Premium Polo Shirt', 'category': 'T-Shirts', 'sizes': ['M', 'L', 'XL'],
             'colors': ['White', 'Blue', 'Red'], 'price': 45.99, 'cost': 22.00},
            {'name': 'Graphic Print Tee', 'category': 'T-Shirts', 'sizes': ['S', 'M', 'L'],
             'colors': ['Black', 'White'], 'price': 29.99, 'cost': 15.00},

            # Jeans
            {'name': 'Slim Fit Jeans', 'category': 'Jeans', 'sizes': ['28', '30', '32', '34', '36'],
             'colors': ['Blue', 'Black', 'Gray'], 'price': 79.99, 'cost': 40.00},
            {'name': 'Straight Cut Jeans', 'category': 'Jeans', 'sizes': ['30', '32', '34'],
             'colors': ['Blue', 'Black'], 'price': 69.99, 'cost': 35.00},
            {'name': 'Skinny Jeans', 'category': 'Jeans', 'sizes': ['26', '28', '30', '32'],
             'colors': ['Blue', 'Black', 'White'], 'price': 89.99, 'cost': 45.00},

            # Dresses
            {'name': 'Summer Floral Dress', 'category': 'Dresses', 'sizes': ['S', 'M', 'L'],
             'colors': ['Pink', 'Blue', 'Yellow'], 'price': 65.99, 'cost': 32.00},
            {'name': 'Evening Cocktail Dress', 'category': 'Dresses', 'sizes': ['S', 'M', 'L', 'XL'],
             'colors': ['Black', 'Red', 'Navy'], 'price': 129.99, 'cost': 65.00},
            {'name': 'Casual Midi Dress', 'category': 'Dresses', 'sizes': ['M', 'L'], 'colors': ['Gray', 'Beige'],
             'price': 55.99, 'cost': 28.00},

            # Jackets
            {'name': 'Denim Jacket', 'category': 'Jackets', 'sizes': ['S', 'M', 'L', 'XL'], 'colors': ['Blue', 'Black'],
             'price': 89.99, 'cost': 45.00},
            {'name': 'Leather Jacket', 'category': 'Jackets', 'sizes': ['M', 'L', 'XL'], 'colors': ['Black', 'Brown'],
             'price': 199.99, 'cost': 100.00},
            {'name': 'Windbreaker', 'category': 'Jackets', 'sizes': ['S', 'M', 'L'],
             'colors': ['Navy', 'Gray', 'Green'], 'price': 75.99, 'cost': 38.00},
        ]

        for product_data in products_data:
            category = Category.objects.get(name=product_data['category'])
            for size in product_data['sizes']:
                for color in product_data['colors']:
                    sku = f"{product_data['name'][:3].upper()}-{size}-{color[:3].upper()}-{random.randint(100, 999)}"
                    product, created = Product.objects.get_or_create(
                        name=product_data['name'],
                        category=category,
                        size=size,
                        color=color,
                        defaults={
                            'price': Decimal(str(product_data['price'])),
                            'cost_price': Decimal(str(product_data['cost'])),
                            'stock_quantity': random.randint(10, 100),
                            'sku': sku,
                            'description': f"{product_data['name']} in {color} color, size {size}"
                        }
                    )
                    if created:
                        self.stdout.write(f'Created product: {product.name} - {size} - {color}')

        # Create customers
        customers_data = [
            {'name': 'John Smith', 'email': 'john.smith@email.com', 'phone': '+1234567890',
             'address': '123 Main St, New York, NY 10001'},
            {'name': 'Sarah Johnson', 'email': 'sarah.j@email.com', 'phone': '+1234567891',
             'address': '456 Oak Ave, Los Angeles, CA 90210'},
            {'name': 'Mike Wilson', 'email': 'mike.wilson@email.com', 'phone': '+1234567892',
             'address': '789 Pine St, Chicago, IL 60601'},
            {'name': 'Emily Davis', 'email': 'emily.davis@email.com', 'phone': '+1234567893',
             'address': '321 Elm St, Houston, TX 77001'},
            {'name': 'David Brown', 'email': 'david.brown@email.com', 'phone': '+1234567894',
             'address': '654 Maple Ave, Phoenix, AZ 85001'},
            {'name': 'Lisa Garcia', 'email': 'lisa.garcia@email.com', 'phone': '+1234567895',
             'address': '987 Cedar St, Philadelphia, PA 19101'},
            {'name': 'James Miller', 'email': 'james.miller@email.com', 'phone': '+1234567896',
             'address': '147 Birch Ave, San Antonio, TX 78201'},
            {'name': 'Anna Martinez', 'email': 'anna.martinez@email.com', 'phone': '+1234567897',
             'address': '258 Spruce St, San Diego, CA 92101'},
            {'name': 'Robert Taylor', 'email': 'robert.taylor@email.com', 'phone': '+1234567898',
             'address': '369 Willow Ave, Dallas, TX 75201'},
            {'name': 'Jennifer Anderson', 'email': 'jennifer.anderson@email.com', 'phone': '+1234567899',
             'address': '741 Poplar St, San Jose, CA 95101'},
        ]

        admin_user = User.objects.get(username='admin')

        for customer_data in customers_data:
            customer, created = Customer.objects.get_or_create(
                email=customer_data['email'],
                defaults=customer_data
            )
            if created:
                self.stdout.write(f'Created customer: {customer.name}')

        # Create sales
        customers = Customer.objects.all()
        products = Product.objects.all()
        payment_methods = ['cash', 'card', 'transfer']

        for i in range(50):  # Create 50 sales
            customer = random.choice(customers)
            payment_method = random.choice(payment_methods)

            sale = Sale.objects.create(
                customer=customer,
                total_amount=Decimal('0.00'),
                payment_method=payment_method,
                notes=f'Sale #{i + 1} - {customer.name}',
                created_by=admin_user,
                sale_date=timezone.now() - timezone.timedelta(days=random.randint(0, 90))
            )

            # Add 1-5 items to each sale
            total_amount = Decimal('0.00')
            num_items = random.randint(1, 5)

            for j in range(num_items):
                product = random.choice(products)
                quantity = random.randint(1, 3)

                if product.stock_quantity >= quantity:
                    sale_item = SaleItem.objects.create(
                        sale=sale,
                        product=product,
                        quantity=quantity,
                        unit_price=product.price,
                        total_price=quantity * product.price
                    )

                    # Update stock
                    product.stock_quantity -= quantity
                    product.save()

                    total_amount += sale_item.total_price

            sale.total_amount = total_amount
            sale.save()

        self.stdout.write(f'Created {Sale.objects.count()} sales')

        # Create expenses
        expense_types = ['rent', 'utilities', 'marketing', 'supplies', 'other']
        expense_descriptions = [
            'Monthly store rent',
            'Electricity bill',
            'Social media advertising',
            'Office supplies',
            'Equipment maintenance',
            'Internet and phone',
            'Marketing materials',
            'Store cleaning',
            'Insurance payment',
            'Staff training'
        ]

        for i in range(20):  # Create 20 expenses
            expense = Expense.objects.create(
                description=random.choice(expense_descriptions),
                amount=Decimal(str(random.uniform(50, 2000))),
                expense_type=random.choice(expense_types),
                date=timezone.now() - timezone.timedelta(days=random.randint(0, 90)),
                created_by=admin_user
            )

        self.stdout.write(f'Created {Expense.objects.count()} expenses')
        self.stdout.write(self.style.SUCCESS('Successfully populated database with dummy data!'))
        self.stdout.write('You can now login with username: admin, password: admin123')
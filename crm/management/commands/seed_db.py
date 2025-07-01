import random
from decimal import Decimal
from django.utils import timezone

from crm.models import Customer, Product, Order

# Clear old data
Customer.objects.all().delete()
Product.objects.all().delete()
Order.objects.all().delete()

# Seed Customers
customers = [
    Customer(name="Alice Johnson", email="alice@example.com", phone="+1234567890"),
    Customer(name="Bob Smith", email="bob@example.com", phone="123-456-7890"),
    Customer(name="Carol Danvers", email="carol@example.com", phone="111-222-3333"),
]
Customer.objects.bulk_create(customers)

# Seed Products
products = [
    Product(name="Laptop", price=Decimal("999.99"), stock=10),
    Product(name="Smartphone", price=Decimal("599.99"), stock=20),
    Product(name="Headphones", price=Decimal("199.99"), stock=15),
    Product(name="Mouse", price=Decimal("49.99"), stock=50),
]
Product.objects.bulk_create(products)

# Re-fetch for ID access
customers = list(Customer.objects.all())
products = list(Product.objects.all())

# Update Order model if needed to support ManyToMany
try:
    for i in range(5):
        customer = random.choice(customers)
        selected_products = random.sample(products, k=2)
        total_amount = sum(p.price for p in selected_products)
        order = Order.objects.create(
            customer=customer,
            order_date=timezone.now(),
            total_amount=total_amount
        )
        order.products.set(selected_products)
except AttributeError:
    print("⚠️ Make sure your Order model has a ManyToManyField to Product and a total_amount field!")

print("✅ Database seeded successfully.")

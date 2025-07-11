#!/bin/bash
PROJECT_DIR="/mnt/c/Users/MR. EMMANUEL/Desktop/alx-backend-graphql_crm"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
DELETED_COUNT=$("$PROJECT_DIR/venv/bin/python" "$PROJECT_DIR/manage.py" shell -c "
from crm.models import Customer
from django.utils import timezone
from datetime import timedelta
cutoff = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.exclude(order__order_date__gte=cutoff).distinct()
count = inactive_customers.count()
inactive_customers.delete()
print(count)
")

echo "$TIMESTAMP - Deleted $DELETED_COUNT inactive customers" >> /tmp/customer_cleanup_log.txt

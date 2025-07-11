#!/bin/bash

# Set working directory to the script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$PROJECT_DIR" || exit 1

# Check if venv python exists before running
if [ -x "$PROJECT_DIR/venv/bin/python" ]; then
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

    DELETED_COUNT=$("$PROJECT_DIR/venv/bin/python" manage.py shell -c "
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
else
    echo "Python environment not found!" >&2
fi

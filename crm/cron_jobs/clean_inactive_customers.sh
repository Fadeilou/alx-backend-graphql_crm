#!/bin/bash

# Absolute path to the project's manage.py
MANAGE_PY_PATH="/home/fadel/Workspaces/ALX PROJECT/alx-backend-graphql_crm/manage.py"
LOG_FILE="/tmp/customer_cleanup_log.txt"

# Python script to be executed
PYTHON_SCRIPT="
from django.utils import timezone;
from datetime import timedelta;
from crm.models import Customer;
from django.db.models import Max;

one_year_ago = timezone.now() - timedelta(days=365);

customers_with_old_orders = Customer.objects.annotate(last_order_date=Max('orders__order_date')).filter(last_order_date__lt=one_year_ago);
customers_with_no_orders = Customer.objects.filter(orders__isnull=True);

inactive_customers_to_delete = customers_with_old_orders.union(customers_with_no_orders);

count = inactive_customers_to_delete.count();
if count > 0:
    inactive_customers_to_delete.delete();

print(count);
"

# Execute the Django management command
DELETED_COUNT=$(echo "$PYTHON_SCRIPT" | python $MANAGE_PY_PATH shell)

# Log the result
echo "$(date): Deleted $DELETED_COUNT inactive customers." >> $LOG_FILE

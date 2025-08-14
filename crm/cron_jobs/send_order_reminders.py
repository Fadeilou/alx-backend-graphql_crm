import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# GraphQL query
query = gql("""
    query {
        allOrders {
            orderId
            orderDate
            customer {
                email
            }
        }
    }
""")

# Setup client
transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
client = Client(transport=transport, fetch_schema_from_transport=True)

# Execute query
result = client.execute(query)

# Filter orders from the last 7 days
seven_days_ago = datetime.datetime.now() - datetime.timedelta(days=7)
log_entries = []

for order in result['allOrders']:
    order_date = datetime.datetime.fromisoformat(order['orderDate'])
    if order_date > seven_days_ago:
        log_entry = f"Order ID: {order['orderId']}, Customer Email: {order['customer']['email']}"
        log_entries.append(log_entry)

# Log to file
with open("/tmp/order_reminders_log.txt", "a") as f:
    timestamp = datetime.datetime.now().isoformat()
    f.write(f"--- {timestamp} ---\n")
    for entry in log_entries:
        f.write(f"{entry}\n")

print("Order reminders processed!")

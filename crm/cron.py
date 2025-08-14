import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    """
    Logs a heartbeat message to a file.
    """
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_message = f"{timestamp} CRM is alive\n"

    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(log_message)

    # Optional: Query the GraphQL hello field
    try:
        transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql('''
            query {
                hello
            }
        ''')
        result = client.execute(query)
        # You can log the result if needed
        # print(result)
    except Exception as e:
        # Log any errors during the GraphQL query
        with open("/tmp/crm_heartbeat_log.txt", "a") as f:
            f.write(f"Error querying GraphQL: {e}\n")


def update_low_stock():
    """
    Executes the UpdateLowStockProducts mutation and logs the result.
    """
    transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
    client = Client(transport=transport, fetch_schema_from_transport=True)

    mutation = gql("""
        mutation {
            updateLowStockProducts {
                updatedProducts {
                    name
                    stock
                }
                message
            }
        }
    """)

    result = client.execute(mutation)

    with open("/tmp/low_stock_updates_log.txt", "a") as f:
        timestamp = datetime.datetime.now().isoformat()
        f.write(f"--- {timestamp} ---")
        if 'data' in result and result['data']['updateLowStockProducts']:
            updated_products = result['data']['updateLowStockProducts']['updatedProducts']
            for product in updated_products:
                f.write(f"Updated {product['name']}: new stock {product['stock']}")
        else:
            f.write("No products updated or an error occurred.")



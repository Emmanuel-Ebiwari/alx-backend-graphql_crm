#!/usr/bin/env python3

import requests
from datetime import datetime, timedelta
import json

GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"
LOG_FILE = "/tmp/order_reminders_log.txt"

query = """
query GetRecentOrders($since: DateTime!) {
  orders(orderDate_Gte: $since) {
    id
    customer {
      email
    }
  }
}
"""

def main():
    since_date = (datetime.utcnow() - timedelta(days=7)).isoformat()
    response = requests.post(
        GRAPHQL_ENDPOINT,
        json={
            "query": query,
            "variables": {"since": since_date}
        },
        headers={"Content-Type": "application/json"}
    )

    data = response.json()

    with open(LOG_FILE, "a") as log_file:
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        orders = data.get("data", {}).get("orders", [])
        for order in orders:
            log_line = f"{timestamp} - Order ID: {order['id']}, Customer Email: {order['customer']['email']}\n"
            log_file.write(log_line)

    print("Order reminders processed!")

if __name__ == "__main__":
    main()

import click
from storage import load_data, save_data

@click.group(help="Commands for managing orders.")
def orders():
    """Order management commands."""
    pass

@orders.command(help="Add a new order for a customer.")
@click.argument("customer_name", type=str)
@click.argument("order", type=(str, float, str))
def add(customer_name, order):
    """Adds a new order (product, price, category) to a specific customer."""
    if not customer_name:
        print("Customer name is required")
        return

    if not order:
        print("Order is required")
        return

    data = load_data()
    customers = data.get("customers", [])

    if customer_name not in customers:
        print("Customer not found")
        return

    data.setdefault("orders", {})
    data["orders"].setdefault(customer_name, [])
    data["orders"][customer_name].append(order)

    save_data(data)

    print(f"Order: {order} for {customer_name} added")

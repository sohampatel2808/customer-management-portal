import click
from storage import load_data, save_data
from utility import pluralize

@click.group(help="Commands for managing customers.")
def customers():
    """Customer management commands."""
    pass

@customers.command(help="Add a new customer.")
@click.argument("name", type=str)
def add(name):
    """Adds a new customer by name to the database."""
    if not name:
        print("Customer name is required")
        return

    data = load_data()
    data.setdefault("customers", [])
    
    if name in data["customers"]:
        print(f"Customer '{name}' already exists.")
        return

    data["customers"].append(name)
    save_data(data)

    print(f"Customer added: {name}")

@customers.command(name='list', help="List all customers.")
def show():
    """Shows a list of all saved customers."""
    data = load_data()
    customers = data.get("customers", [])

    if not customers:
        print("No customer found")
        return

    word = pluralize(len(customers), "customer")
    print(f"Here is the list of {word}:")

    for cust_name in customers:
        print(f"- {cust_name}")

@customers.command(help="Show a summary of customer spending and categories.")
def summary():
    """Displays a total summary of each customer's spending and order categories."""
    data = load_data()
    orders = data.get("orders", {})

    if not orders:
        print("No orders found for summary.")
        return

    for cust_name, cust_orders in orders.items():
        categories = {}
        total_spending = 0

        for product, price, category in cust_orders:
            total_spending += price
            categories[category] = categories.get(category, 0) + price

        print(f"{cust_name}:")
        print(f"  - Total Spending: {total_spending}")
        print(f"  - Categories: {categories}")

@customers.command(help="Filter customers by a specific product name.")
@click.argument("product_name", type=str)
def filter_by_product(product_name):
    """Finds and lists all customers that have purchased the specified product."""
    data = load_data()
    orders = data.get("orders", {})

    customers = [
        cust_name
        for cust_name, cust_orders in orders.items()
        for product, price, category in cust_orders
        if product == product_name
    ]

    print(f"Customers who have purchased {product_name}: {customers}")

@customers.command(help="Group customers into high, moderate, and low spending tiers.")
def group_by_spending():
    """Analyzes customer spending and categorizes them into spending tiers."""
    customers_high = []
    customers_moderate = []
    customers_low = []

    data = load_data()
    orders = data.get("orders", {})

    for cust_name, cust_orders in orders.items():
        total_spending = sum(order[1] for order in cust_orders)

        if total_spending > 100:
            customers_high.append(cust_name)
        elif total_spending > 50:
            customers_moderate.append(cust_name)
        else:
            customers_low.append(cust_name)

    print("Here is the analysis of customers by spending:")
    print(f"High: {customers_high}")
    print(f"Moderate: {customers_moderate}")
    print(f"Low: {customers_low}")

@customers.command(help="Sort top 3 customers by their total spending.")
@click.option('--order-by', default='D', help="A for ascending, D for descending")
def top_by_spending(order_by):
    """Retrieves the top 3 customers sorted by their lifetime spending."""
    customers = {}
    
    data = load_data()
    orders = data.get("orders", {})

    for cust_name, cust_orders in orders.items():
        customers[cust_name] = sum(price for product, price, category in cust_orders)

    reverse = order_by != 'A'
    customers_sorted = dict(
        sorted(customers.items(), key=lambda x: x[1], reverse=reverse)
    )
    top_3 = dict(list(customers_sorted.items())[:3])

    print(f"Customers are sorted in {order_by} order by their spending: {top_3}")

@customers.command(help="Find customers by multiple purchased categories.")
@click.option('--category-names', default='', help="Comma separated list of categories to filter by.")
def filter_by_multiple_categories(category_names):
    """Finds customers who have placed orders across multiple distinct categories."""
    data = load_data()
    orders = data.get("orders", {})

    categories = [c.strip().lower() for c in category_names.split(",") if c.strip()]

    customers = [
        cust_name
        for cust_name, cust_orders in orders.items()
        if len(
            set(
                category
                for _, _, category in cust_orders
                if not categories or category.lower() in categories
            )
        ) > 1
    ]

    filter_text = f"multiple {categories}" if categories else "ALL Categories"
    print(f"Customers with orders from {filter_text}: {customers}")

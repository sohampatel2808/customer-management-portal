import click
from storage import load_data, save_data
from utility import pluralize

@click.group()
def customers():
    pass

@customers.command()
@click.argument("name", type=str)
def add(name):
    if not name:
        print("Customer name is required")
        return

    data = load_data()

    data.setdefault("customers", [])
    data["customers"].append(name)

    save_data(data)

    print(f"Customer added: {name}")

@customers.command(name='list')
def show():
    data = load_data()
    customers = data.get("customers", [])

    if not customers:
        print("No customer found")
        return

    word = pluralize(len(customers), "customer")
    print(f"Here is the list of {word}:")

    for cust_name in customers:
        print(f"- {cust_name}")

@customers.command()
def summary():
    data = load_data()
    orders = data.get("orders", {})

    for cust_name, cust_orders in orders.items():
        categories = {}
        total_spending = 0

        for product, price, category in cust_orders:
            total_spending += price
            categories[category] = categories.get(category, 0) + price

        print(f"{cust_name}:")
        print(f"  - Total Spending: {total_spending}")
        print(f"  - Categories: {categories}")

@customers.command()
@click.argument("product_name", type=str)
def filter_by_product(product_name):
    data = load_data()
    orders = data.get("orders", {})

    customers = [
        cust_name
        for cust_name, cust_orders in orders.items()
        for product, price, category in cust_orders
        if product == product_name
    ]

    print(f"Customers who has purchased {product_name}: {customers}")

@customers.command()
def group_by_spending():
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

@customers.command()
@click.option('--order-by', default='D', help="A for ascending, D for descending")
def sort_by_spending(order_by):
    customers = {}
    customers_sorted = {}

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

@customers.command()
@click.option('--category-names', default='', help="")
def order_from_multiple_categories(category_names):
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

    print(f"Customers with more than multiple {categories or 'ALL'}: {customers}")

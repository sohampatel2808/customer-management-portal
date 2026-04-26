import click
from storage import load_data, save_data
from utility import pluralize

@click.group()
def products():
    pass

@products.command()
def list_categories():
    categories = []

    data = load_data()
    orders = data.get("orders", {})

    for cust_orders in orders.values():
        categories.append(category for product, price, category in cust_orders)

    uniq_categories = list(set(categories))

    word = pluralize(len(uniq_categories), "category", "categories")
    print(f"Here is the list of unique {word}: {uniq_categories}")

@products.command()
def revenue_per_category():
    categories = {}

    data = load_data()
    orders = data.get("orders", {})

    for cust_orders in orders.values():
        for product, price, category in cust_orders:
            categories[category] = categories.get(category, 0) + price

    print(f"Revenue per category: {categories}")

@products.command(name='list')
def show():
    products = []

    data = load_data()
    orders = data.get("orders", {})

    for cust_orders in orders.values():
        products.append(product for product, price, category in cust_orders)

    uniq_products = list(set(products))

    word = pluralize(len(uniq_products), "product")
    print(f"Here is the list of unique {word}: {uniq_products}")

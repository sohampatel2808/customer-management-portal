import click
from commands.customers import customers
from commands.orders import orders
from commands.products import products

@click.group()
def cli():
    pass

cli.add_command(customers)
cli.add_command(orders)
cli.add_command(products)

if __name__ == "__main__":
    cli()

import click
from commands.customers import customers
from commands.orders import orders
from commands.products import products

@click.group(help="Main entry point for the CLI tracking system.")
def cli():
    """A python CLI project to manage customers, orders, and products."""
    pass

cli.add_command(customers)
cli.add_command(orders)
cli.add_command(products)

if __name__ == "__main__":
    cli()

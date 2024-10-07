import sys
# import os

import click

# # Add the parent directory to sys.path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.config import authenticate
from src.dropbox_utils import print_namespaces, print_members
from src.scrape import scrape

# Create the Click group
@click.group()
def cli():
    """Dropbox Utility CLI to authenticate, list namespaces, and list members."""
    pass

# Command for authentication
@cli.command()
def auth():
    """Authenticate the user."""
    click.echo("Authenticating the user...")
    authenticate()  # Call the authentication function from src.config

# Command for listing namespaces
@cli.command()
def namespaces():
    """List Dropbox namespaces."""
    click.echo("Listing namespaces...")
    print_namespaces()  # Call the function from src.dropbox_utils

# Command for listing members
@cli.command()
def members():
    """List Dropbox members."""
    click.echo("Listing team members...")
    print_members()  # Call the function from src.dropbox_utils

# Command for scraping
@cli.command()
@click.option('--namespace', '-n', default=None, help='Namespace to scrape files from.')
@click.option('--output', '-o', default=None, help='File to save the output.')
def scrape_command(namespace, output):
    """Scrape files and metadata from a specific namespace."""
    click.echo(f"Scraping from namespace: {namespace}")
    click.echo(f"Saving output to: {output}")
    # Call the scrape function with optional namespace and output arguments
    scrape(namespace=namespace, output=output)


# Main entry point for the CLI
if __name__ == '__main__':
    cli()

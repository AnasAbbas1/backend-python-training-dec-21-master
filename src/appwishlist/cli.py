import click
import logging

logger = logging.getLogger(__name__)


@click.group()
def cli():
    pass


@cli.group()
def db():
    pass


@db.command()
def create():
    from libwishlist import models

    models.tables.create_all()


if __name__ == "__main__":
    cli()

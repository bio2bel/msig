# -*- coding: utf-8 -*-

from __future__ import print_function

import logging
import os

import click
from pandas import DataFrame, Series

from .constants import DEFAULT_CACHE_CONNECTION
from .manager import Manager

log = logging.getLogger(__name__)


def set_debug(level):
    logging.basicConfig(level=level, format="%(asctime)s - %(levelname)s - %(message)s")


def set_debug_param(debug):
    if debug == 0:
        set_debug(30)
    elif debug == 1:
        set_debug(20)
    elif debug == 2:
        set_debug(10)


@click.group()
def main():
    """Bio2BEL MSIG"""
    logging.basicConfig(level=10, format="%(asctime)s - %(levelname)s - %(message)s")


@main.command()
@click.option('-v', '--debug', count=True, help="Turn on debugging.")
@click.option('-c', '--connection', help="Defaults to {}".format(DEFAULT_CACHE_CONNECTION))
@click.option('-p', '--path', help="Custom path to gene set file")
@click.option('-d', '--delete_first', is_flag=True)
def populate(debug, connection, path, delete_first):
    """Build the local version of the repo."""
    set_debug_param(debug)

    m = Manager(connection=connection)

    if delete_first or click.confirm('Drop first the database?'):
        m.drop_all()
        m.create_all()

    click.echo("populate tables")
    m.populate(path=path)


@main.command()
@click.option('-v', '--debug', count=True, help="Turn on debugging.")
@click.option('-y', '--yes', is_flag=True)
@click.option('-c', '--connection', help="Defaults to {}".format(DEFAULT_CACHE_CONNECTION))
def drop(debug, yes, connection):
    """Drop the repo."""

    set_debug_param(debug)

    if yes or click.confirm('Do you really want to delete the database?'):
        m = Manager(connection=connection)
        click.echo("drop db")
        m.drop_all()


@main.command()
@click.option('-c', '--connection', help="Defaults to {}".format(DEFAULT_CACHE_CONNECTION))
def export(connection):
    """Export all pathway - gene info to a excel file"""
    m = Manager(connection=connection)

    log.info("Querying the database")

    # https://stackoverflow.com/questions/19736080/creating-dataframe-from-a-dictionary-where-entries-have-different-lengths
    genesets = DataFrame(
        dict([
            (k, Series(list(v)))
            for k, v in m.export_genesets().items()
        ])
    )

    log.info("Geneset exported to '{}/msig_gene_sets.xlsx'".format(os.getcwd()))

    genesets.to_excel('msig_gene_sets.xlsx', index=False)


@main.command()
@click.option('-c', '--connection', help="Defaults to {}".format(DEFAULT_CACHE_CONNECTION))
def web(connection):
    """Run web"""
    from .web import create_app
    app = create_app(connection=connection)
    app.run(host='0.0.0.0', port=5000)

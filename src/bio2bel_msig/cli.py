# -*- coding: utf-8 -*-

from __future__ import print_function

import logging
import os

import click
from bio2bel import build_cli
from pandas import DataFrame, Series

from .constants import DEFAULT_CACHE_CONNECTION
from .manager import Manager

log = logging.getLogger(__name__)

main = build_cli(Manager)


@main.command()
@click.option('-c', '--connection', help="Defaults to {}".format(DEFAULT_CACHE_CONNECTION))
@click.option('-p', '--path', help="Custom path to gene set file")
@click.option('-d', '--delete_first', is_flag=True)
def populate(connection, path, delete_first):
    """Build the local version of the repo."""

    m = Manager(connection=connection)

    if delete_first or click.confirm('Drop first the database?'):
        m.drop_all()
        m.create_all()

    click.echo("populate tables")
    m.populate(path=path)


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

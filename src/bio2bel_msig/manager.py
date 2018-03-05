# -*- coding: utf-8 -*-

"""
This module populates the tables of Bio2BEL MSIG
"""

import logging

from bio2bel.utils import get_connection
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm

from .constants import MODULE_NAME
from .models import Base, Pathway, Protein

__all__ = [
    'Manager'
]

log = logging.getLogger(__name__)


class Manager(object):
    """Database manager"""

    def __init__(self, connection=None):
        self.connection = get_connection(MODULE_NAME, connection)
        self.engine = create_engine(self.connection)
        self.session_maker = sessionmaker(bind=self.engine, autoflush=False, expire_on_commit=False)
        self.session = self.session_maker()
        self.create_all()

    def create_all(self, check_first=True):
        """Create tables for Template"""
        log.info('create table in {}'.format(self.engine.url))
        Base.metadata.create_all(self.engine, checkfirst=check_first)

    def drop_all(self, check_first=True):
        """Drop all tables for Template"""
        log.info('drop tables in {}'.format(self.engine.url))
        Base.metadata.drop_all(self.engine, checkfirst=check_first)

    @staticmethod
    def ensure(connection=None):
        """Checks and allows for a Manager to be passed to the function. """
        if connection is None or isinstance(connection, str):
            return Manager(connection=connection)

        if isinstance(connection, Manager):
            return connection

        raise TypeError

    """Custom query methods"""

    def query_gene_set(self, gene_set):
        """Returns Proteins within the gene set

        :param gene_set: set of gene symbols
        :rtype: list[models.Protein]
        :return: list of proteins
        """

        return self.session.query(Protein).filter(Protein.hgnc_symbol.in_(gene_set)).all()

    def get_pathway_by_id(self, identifier):
        """Gets a pathway by its id

        :param id:  identifier
        :rtype: Optional[Pathway]
        """
        return self.session.query(Pathway).filter(Pathway.id == identifier).one_or_none()

    def get_pathway_by_name(self, pathway_name):
        """Gets a pathway by its name

        :param pathway_name: name
        :rtype: Optional[Pathway]
        """
        return self.session.query(Pathway).filter(Pathway.name == pathway_name).one_or_none()

    def get_all_pathways(self):
        """Gets all pathways stored in the database

        :rtype: list[Pathway]
        """
        return self.session.query(Pathway).all()

    def get_pathway_names_to_ids(self):
        """Returns a dictionary of pathway names to ids

        :rtype: dict[str,str]
        """
        human_pathways = self.get_all_pathways()

        return {
            pathway.name: pathway.id
            for pathway in human_pathways
        }

    def get_all_hgnc_symbols(self):
        """Returns the set of genes present in all Pathways

        :rtype: set
        """
        return {
            gene.hgnc_symbol
            for pathway in self.get_all_pathways()
            for gene in pathway.proteins
            if pathway.proteins
        }

    def get_pathway_size_distribution(self):
        """Returns pathway sizes

        :rtype: dict
        :return: pathway sizes
        """

        pathways = self.get_all_pathways()

        return {
            pathway.name: len(pathway.proteins)
            for pathway in pathways
            if pathway.proteins
        }

    def query_pathway_by_name(self, query, limit=None):
        """Returns all pathways having the query in their names

        :param query: query string
        :param Optional[int] limit: limit result query
        :rtype: list[Pathway]
        """

        q = self.session.query(Pathway).filter(Pathway.name.contains(query))

        if limit:
            q = q.limit(limit)

        return q.all()

    def get_or_create_pathway(self, pathway_name):
        """Gets an pathway from the database or creates it

        :param str pathway_name: pathway ame
        :rtype: Pathway
        """
        pathway = self.get_pathway_by_name(pathway_name)

        if pathway is None:
            pathway = Pathway(
                name=pathway_name
            )
            self.session.add(pathway)

        return pathway

    def get_protein_by_id(self, identifier):
        """Gets a protein by its id

        :param identifier: identifier
        :rtype: Optional[Protein]
        """
        return self.session.query(Protein).filter(Protein.id == identifier).one_or_none()

    def get_or_create_protein(self, hgnc_symbol):
        """Gets an protein from the database or creates it
        :param Optional[str] hgnc_symbol: name of the protein
        :rtype: Protein
        """
        protein = self.get_protein_by_hgnc_symbol(hgnc_symbol)

        if protein is None:
            protein = Protein(
                hgnc_symbol=hgnc_symbol,
            )
            self.session.add(protein)

        return protein

    def get_protein_by_hgnc_symbol(self, hgnc_symbol):
        """Gets a protein by its hgnc symbol

        :param hgnc_id: hgnc identifier
        :rtype: Optional[Protein]
        """
        return self.session.query(Protein).filter(Protein.hgnc_symbol == hgnc_symbol).one_or_none()

    """Methods to populate the DB"""

    def _populate_pathways(self, url=None):
        """Populate pathway table

        :param Optional[str] url: url from pathway table file
        """

        # TODO: add here your parser for the pathway model (see example.py)
        pathways_dict = ...

        for id, name in tqdm(pathways_dict.items(), desc='Loading pathways'):
            pathway = self.get_or_create_pathway(pathway_name=name)

        self.session.commit()

    def _pathway_entity(self, url=None):
        """Populates Protein Tables

        :param Optional[str] url: url from protein to pathway file
        """

        # TODO: add here your parser for the protein model (see example.py)

        protein_pathway_dict = ...

        for hgnc_symbol, pathway_name in tqdm(protein_pathway_dict, desc='Loading proteins'):
            protein = self.get_or_create_protein(hgnc_symbol=hgnc_symbol)

            pathway = self.get_pathway_by_name(pathway_name)

            protein.pathways.append(pathway)

        self.session.commit()

    def populate(self, pathways_url=None, protein_pathway_url=None):
        """Populates all tables"""
        self._populate_pathways(url=pathways_url)
        self._pathway_entity(url=protein_pathway_url)

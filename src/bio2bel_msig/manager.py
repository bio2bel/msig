# -*- coding: utf-8 -*-

"""This module populates the tables of Bio2BEL MSIG."""

import logging
from typing import Optional

from flask_admin.contrib.sqla import ModelView
from tqdm import tqdm

from bio2bel.compath import CompathManager
from .constants import MODULE_NAME
from .models import Base, Pathway, Protein, protein_pathway
from .parser import download, parse_gmt_file

__all__ = [
    'Manager'
]

logger = logging.getLogger(__name__)


class PathwayView(ModelView):
    """Pathway view in Flask-admin."""

    column_searchable_list = (
        Pathway.identifier,
        Pathway.name,
    )


class ProteinView(ModelView):
    """Protein view in Flask-admin."""

    column_searchable_list = (
        Protein.hgnc_symbol,
        Protein.hgnc_id,
    )


class Manager(CompathManager):
    """Gene-gene set memberships."""

    module_name = MODULE_NAME
    _base = Base
    flask_admin_models = [
        (Pathway, PathwayView),
        (Protein, ProteinView),
    ]
    namespace_model = pathway_model = Pathway
    edge_model = protein_pathway
    protein_model = Protein

    def get_or_create_pathway(self, pathway_name: str) -> Pathway:
        """Get a pathway from the database or creates it."""
        pathway = self.get_pathways_by_name(pathway_name)

        if pathway is None:
            pathway = Pathway(
                name=pathway_name,
                identifier=pathway_name,
            )
            self.session.add(pathway)

        return pathway

    def get_or_create_protein(self, hgnc_symbol: str) -> Protein:
        """Get an protein from the database or creates it."""
        protein = self.get_protein_by_hgnc_symbol(hgnc_symbol)

        if protein is None:
            protein = Protein(
                hgnc_symbol=hgnc_symbol,
            )
            self.session.add(protein)

        return protein

    def populate(self, path: Optional[str] = None) -> None:
        """Populate all tables.

        :param path: Path to a custom GMT file
        """
        download()
        pathways = parse_gmt_file(path=path)
        if not pathways:
            raise FileNotFoundError(
                'No pathways found. Please ensure that the selected gene set file contains pathways.'
            )

        hgnc_symbols = {
            hgnc_symbol
            for _, _, hgnc_symbols in pathways
            for hgnc_symbol in hgnc_symbols
        }

        hgnc_symbol_to_model = {
            hgnc_symbol: Protein(hgnc_symbol=hgnc_symbol)
            for hgnc_symbol in tqdm(hgnc_symbols, desc='MSig genes')
        }

        self.session.add_all(list(hgnc_symbol_to_model.values()))
        self.session.commit()

        pathway_name_to_model = {
            name: Pathway(
                name=name,
                identifier=name,
                proteins=[
                    hgnc_symbol_to_model[hgnc_symbol]
                    for hgnc_symbol in hgnc_symbols
                ],
            )
            for name, _, hgnc_symbols in tqdm(pathways, desc='MSig pathways')
        }

        self.session.add_all(list(pathway_name_to_model.values()))
        self.session.commit()

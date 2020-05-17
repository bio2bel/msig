# -*- coding: utf-8 -*-

"""This module populates the tables of Bio2BEL MSIG."""

import logging
from typing import Mapping, Optional

from pybel import BELGraph
from pybel.manager.models import Namespace, NamespaceEntry
from tqdm import tqdm

from bio2bel.compath import CompathManager
from .constants import MODULE_NAME
from .models import Base, Pathway, Protein, protein_pathway
from .parser import download, parse_gmt_file

__all__ = [
    'Manager'
]

logger = logging.getLogger(__name__)


class Manager(CompathManager):
    """Gene-gene set memberships."""

    module_name = MODULE_NAME
    _base = Base
    flask_admin_models = [Pathway, Protein]
    namespace_model = pathway_model = Pathway
    edge_model = protein_pathway
    protein_model = Protein
    pathway_model_identifier_column = Pathway.msig_id

    def summarize(self) -> Mapping[str, int]:
        """Summarize the database."""
        return dict(
            pathways=self._count_model(Pathway),
            proteins=self._count_model(Protein),
        )

    """Custom query methods"""

    def get_or_create_pathway(self, pathway_name: str) -> Pathway:
        """Get a pathway from the database or creates it."""
        pathway = self.get_pathway_by_name(pathway_name)

        if pathway is None:
            pathway = Pathway(
                name=pathway_name,
                msig_id=pathway_name,
            )
            self.session.add(pathway)

        return pathway

    def get_protein_by_id(self, identifier: str) -> Optional[Protein]:
        """Get a protein by its id."""
        return self.session.query(Protein).filter(Protein.id == identifier).one_or_none()

    def get_or_create_protein(self, hgnc_symbol: str) -> Protein:
        """Get an protein from the database or creates it."""
        protein = self.get_protein_by_hgnc_symbol(hgnc_symbol)

        if protein is None:
            protein = Protein(
                hgnc_symbol=hgnc_symbol,
            )
            self.session.add(protein)

        return protein

    def get_protein_by_hgnc_symbol(self, hgnc_symbol: str) -> Optional[Protein]:
        """Get a protein by its hgnc symbol"""
        return self.session.query(Protein).filter(Protein.hgnc_symbol == hgnc_symbol).one_or_none()

    def _create_namespace_entry_from_model(self, model: Pathway, namespace: Namespace) -> NamespaceEntry:
        """Create a namespace entry from the model."""
        return NamespaceEntry(encoding='B', name=model.name, identifier=model.msig_id, namespace=namespace)

    @staticmethod
    def _get_identifier(model: Pathway) -> str:
        """Extract the identifier from a pathway mode."""
        return model.msig_id

    def to_bel(self) -> BELGraph:
        """Serialize MSIG to BEL."""
        graph = BELGraph(
            name='MSIG Pathway Definitions',
            version='1.0.0',
        )
        for pathway in self.list_pathways():
            self._add_pathway_to_graph(graph, pathway)
        return graph

    """Methods to populate the DB"""

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
                msig_id=name,
                proteins=[
                    hgnc_symbol_to_model[hgnc_symbol]
                    for hgnc_symbol in hgnc_symbols
                ],
            )
            for name, _, hgnc_symbols in tqdm(pathways, desc='MSig pathways')
        }

        self.session.add_all(list(pathway_name_to_model.values()))
        self.session.commit()

    def _add_admin(self, app, **kwargs):
        from flask_admin import Admin
        from flask_admin.contrib.sqla import ModelView

        class PathwayView(ModelView):
            """Pathway view in Flask-admin"""
            column_searchable_list = (
                Pathway.id,
                Pathway.name
            )

        class ProteinView(ModelView):
            """Protein view in Flask-admin"""
            column_searchable_list = (
                Protein.hgnc_symbol,
                Protein.id
            )

        admin = Admin(app, **kwargs)
        admin.add_view(PathwayView(Pathway, self.session))
        admin.add_view(ProteinView(Protein, self.session))
        return admin

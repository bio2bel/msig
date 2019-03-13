# -*- coding: utf-8 -*-

"""This module populates the tables of Bio2BEL MSIG."""

import logging
import os

from bio2bel.manager.bel_manager import BELManagerMixin
from bio2bel.manager.flask_manager import FlaskMixin
from bio2bel.manager.namespace_manager import BELNamespaceManagerMixin
from compath_utils import CompathManager
from pybel import BELGraph
from pybel.manager.models import NamespaceEntry
from tqdm import tqdm

from .constants import MODULE_NAME
from .models import Base, Pathway, Protein
from .parser import parse_gmt_file

__all__ = [
    'Manager'
]

log = logging.getLogger(__name__)


class Manager(CompathManager, BELNamespaceManagerMixin, BELManagerMixin, FlaskMixin):
    """Bio2BEL MSIG manager."""

    module_name = MODULE_NAME

    flask_admin_models = [Pathway, Protein]
    namespace_model = pathway_model = Pathway
    protein_model = Protein
    pathway_model_identifier_column = Pathway.msig_id

    @property
    def _base(self):
        return Base

    def summarize(self):
        """Summarize the database.

        :rtype: dict[str,int]
        """
        return dict(
            pathways=self._count_model(Pathway),
            proteins=self._count_model(Protein),
        )

    """Custom query methods"""

    def get_or_create_pathway(self, pathway_name):
        """Gets an pathway from the database or creates it

        :param str pathway_name: pathway ame
        :rtype: Pathway
        """
        pathway = self.get_pathway_by_name(pathway_name)

        if pathway is None:
            pathway = Pathway(
                name=pathway_name,
                msig_id=pathway_name
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

    def _create_namespace_entry_from_model(self, model, namespace):
        """Create a namespace entry from the model.

        :param Pathway model: The model to convert
        :type namespace: pybel.manager.models.Namespace
        :rtype: Optional[pybel.manager.models.NamespaceEntry]
        """
        return NamespaceEntry(encoding='B', name=model.name, identifier=model.msig_id, namespace=namespace)

    @staticmethod
    def _get_identifier(model):
        """Extract the identifier from a pathway mode.

        :param Pathway model: The model to convert
        :rtype: str
        """
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

    def populate(self, path=None):
        """Populates all tables

        :param Optional[str] path: url from gmt file
        """
        path = os.environ.get('BIO2BEL_MSIG_PATH')

        if path is None:
            print('Please set an environment variable "BIO2BEL_MSIG_PATH" pointing to the gene set file of MSIG.')
            raise RuntimeError(
                'Please set an environment variable "BIO2BEL_MSIG_PATH" pointing to the gene set file of MSIG.'
            )

        if not os.path.isfile(path):
            print('The "BIO2BEL_MSIG_PATH" variable does not point to any valid file in your system.')
            raise FileNotFoundError(
                'The "BIO2BEL_MSIG_PATH" variable does not point to any valid file in your system.'
            )

        pathways = parse_gmt_file(url=path)

        if not pathways:
            print('No pathways found. Please ensure that the selected gene set file contains pathways.')
            raise FileNotFoundError(
                'No pathways found. Please ensure that the selected gene set file contains pathways.'
            )

        hgnc_symbol_protein = {}

        for pathway_name, _, gene_set in tqdm(pathways, desc='Loading database'):

            pathway = self.get_or_create_pathway(pathway_name=pathway_name)

            for hgnc_symbol in gene_set:

                protein = self.get_or_create_protein(hgnc_symbol)
                hgnc_symbol_protein[hgnc_symbol] = protein

                if pathway not in protein.pathways:
                    protein.pathways.append(pathway)

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

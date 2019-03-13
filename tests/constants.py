# -*- coding: utf-8 -*-
""" This module contains all test constants"""

import os
import tempfile
import unittest

from bio2bel_msig.manager import Manager
from bio2bel_msig.parser import parse_gmt_file

dir_path = os.path.dirname(os.path.realpath(__file__))
resources_path = os.path.join(dir_path, 'resources')

gene_sets_path = os.path.join(resources_path, 'test_gmt_file.gmt')


class DatabaseMixin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create temporary file"""

        cls.fd, cls.path = tempfile.mkstemp()
        cls.connection = 'sqlite:///' + cls.path

        # create temporary database
        cls.manager = Manager(cls.connection)

        # fill temporary database with test data

        pathways = parse_gmt_file(url=gene_sets_path)

        hgnc_symbol_protein = {}

        for pathway_name, _, gene_set in pathways:

            pathway = cls.manager.get_or_create_pathway(pathway_name=pathway_name)

            for hgnc_symbol in gene_set:

                protein = cls.manager.get_or_create_protein(hgnc_symbol)
                hgnc_symbol_protein[hgnc_symbol] = protein

                if pathway not in protein.pathways:
                    protein.pathways.append(pathway)

                    cls.manager.session.commit()

    @classmethod
    def tearDownClass(cls):
        """Closes the connection in the manager and deletes the temporary database"""
        cls.manager.drop_all()
        cls.manager.session.close()
        os.close(cls.fd)
        os.remove(cls.path)

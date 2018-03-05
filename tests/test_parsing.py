# -*- coding: utf-8 -*-
""" This module contains tests for parsing GMT files"""

from bio2bel_msig.models import Pathway, Protein
from tests.constants import DatabaseMixin


class TestParse(DatabaseMixin):
    """Tests the parsing module"""

    def test_pathway_count(self):
        pathway_number = self.manager.session.query(Pathway).count()
        self.assertEqual(3, pathway_number)

    def test_protein_count(self):
        protein_number = self.manager.session.query(Protein).count()
        self.assertEqual(13, protein_number)

    def test_pathway_protein_1(self):
        pathway = self.manager.get_pathway_by_id('AAANWWTGC_UNKNOWN')
        self.assertIsNotNone(pathway, msg='Unable to find pathway')
        self.assertEqual(4, len(pathway.proteins))

        self.assertEqual(
            {'MEF2C', 'ATP1B1', 'RORA', 'PDS5B'},
            {
                gene.hgnc_symbol
                for gene in pathway.proteins
            }
        )

    def test_pathway_protein_2(self):
        pathway = self.manager.get_pathway_by_id('AAAYRNCTG_UNKNOWN')
        self.assertIsNotNone(pathway, msg='Unable to find pathway')
        self.assertEqual(3, len(pathway.proteins))

        self.assertEqual(
            {'LTBP1', 'LEKHM1', 'PDS5B'},
            {
                gene.hgnc_symbol
                for gene in pathway.proteins
            }
        )

    def test_gene_query_1(self):
        """Single protein query. This protein is associated with 1 pathways"""
        enriched_pathways = self.manager.query_gene_set(['KCNE1L'])
        self.assertIsNotNone(enriched_pathways, msg='Enriching function is not working')

        self.assertEqual(
            [
                {
                    "pathway_id": "MYOD_01",
                    "pathway_name": "MYOD_01",
                    "mapped_proteins": 1,
                    "pathway_size": 8,
                }
            ],
            enriched_pathways
        )

    def test_gene_query_2(self):
        """Multiple protein query"""
        enriched_pathways = self.manager.query_gene_set(['PDS5B', 'ATP1B1'])
        self.assertIsNotNone(enriched_pathways, msg='Enriching function is not working')

        self.assertIn(
            {
                "pathway_id": "AAANWWTGC_UNKNOWN",
                "pathway_name": "AAANWWTGC_UNKNOWN",
                "mapped_proteins": 2,
                "pathway_size": 4
            },
            enriched_pathways
        )

        self.assertIn(
            {
                "pathway_id": "AAAYRNCTG_UNKNOWN",
                "pathway_name": "AAAYRNCTG_UNKNOWN",
                "mapped_proteins": 1,
                "pathway_size": 3
            },
            enriched_pathways
        )

        self.assertIn(
            {
                "pathway_id": "MYOD_01",
                "pathway_name": "MYOD_01",
                "mapped_proteins": 1,
                "pathway_size": 8
            },
            enriched_pathways
        )
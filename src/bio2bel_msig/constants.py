# -*- coding: utf-8 -*-

"""This module contains all the constants used in Bio2BEL MSIGDB"""

import os

from bio2bel.utils import get_connection, get_data_dir

MODULE_NAME = 'msig'
DATA_DIR = get_data_dir(MODULE_NAME)
DEFAULT_CACHE_CONNECTION = get_connection(MODULE_NAME)

CONFIG_FILE_PATH = os.path.join(DATA_DIR, 'config.ini')

PATHWAY_LINK = 'http://www.broadinstitute.org/gsea/msigdb/cards/{}'

RESOURCES_PATH = os.path.abspath(os.path.join(__file__, "../../.."))

GENE_SETS_PATH = os.path.join(DATA_DIR, 'resources', 'gene_sets.gmt')

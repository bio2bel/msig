# -*- coding: utf-8 -*-

"""This module contains all the constants used in Bio2BEL MSIGDB"""

import os

from bio2bel.utils import get_connection, get_data_dir

MODULE_NAME = 'msig'
DATA_DIR = get_data_dir(MODULE_NAME)
DEFAULT_CACHE_CONNECTION = get_connection(MODULE_NAME)

CONFIG_FILE_PATH = os.path.join(DATA_DIR, 'config.ini')

MOTIF_GENE_SETS = 'http://software.broadinstitute.org/gsea/msigdb/download_file.jsp?filePath=/resources/msigdb/6.1/c3.all.v6.1.symbols.gmt'

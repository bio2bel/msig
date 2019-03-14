# -*- coding: utf-8 -*-

"""This module contains all the constants used in Bio2BEL MSigDB."""

import os

from bio2bel import get_data_dir

MODULE_NAME = 'msig'
DATA_DIR = get_data_dir(MODULE_NAME)

PATHWAY_LINK = 'http://www.broadinstitute.org/gsea/msigdb/cards/{}'

GMT_ENTREZ_URL = 'http://software.broadinstitute.org/gsea/msigdb/download_file.jsp?filePath=/resources/msigdb/6.2/msigdb.v6.2.entrez.gmt'
GMT_HGNC_SYMBOLS_URL = 'http://software.broadinstitute.org/gsea/msigdb/download_file.jsp?filePath=/resources/msigdb/6.2/msigdb.v6.2.symbols.gmt'

GMT_ENTREZ_PATH = os.path.join(DATA_DIR, GMT_ENTREZ_URL.split('/')[-1])
GMT_HGNC_SYMBOLS_PATH = os.path.join(DATA_DIR, GMT_HGNC_SYMBOLS_URL.split('/')[-1])

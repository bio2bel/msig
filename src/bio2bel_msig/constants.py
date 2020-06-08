# -*- coding: utf-8 -*-

"""This module contains all the constants used in Bio2BEL MSigDB."""

import os

from bio2bel import get_data_dir

MODULE_NAME = 'msig'
DATA_DIR = get_data_dir(MODULE_NAME)

VERSION = '7.1'

PATHWAY_LINK = 'http://www.broadinstitute.org/gsea/msigdb/cards/{}'

DOWNLOAD_BASE = 'https://www.gsea-msigdb.org/gsea/msigdb/download_file.jsp?filePath=/msigdb/release'
GMT_ENTREZ_URL = f'{DOWNLOAD_BASE}/{VERSION}/msigdb.v{VERSION}.entrez.gmt'
GMT_HGNC_SYMBOLS_URL = f'{DOWNLOAD_BASE}/{VERSION}/msigdb.v{VERSION}.symbols.gmt'

GMT_ENTREZ_PATH = os.path.join(DATA_DIR, GMT_ENTREZ_URL.split('/')[-1])
GMT_HGNC_SYMBOLS_PATH = os.path.join(DATA_DIR, GMT_HGNC_SYMBOLS_URL.split('/')[-1])

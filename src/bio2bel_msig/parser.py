# -*- coding: utf-8 -*-

"""Parsers for Bio2BEL MSig."""

import logging
import os
from typing import List, Optional, Set, Tuple

from pyobo.sources.msig import GMT_ENTREZ_PATH, GMT_HGNC_PATH, ensure_msig_path

__all__ = [
    'parse_gmt_file',
    'download',
]

logger = logging.getLogger(__name__)


def download(force: bool = False) -> None:
    if not has_files() or force:
        ensure_msig_path()


def has_files() -> bool:
    return os.path.exists(GMT_ENTREZ_PATH) and os.path.exists(GMT_HGNC_PATH)


def _process_line(line: str) -> Tuple[str, str, Set[str]]:
    """Return the pathway name, url, and gene sets associated.

    :param line: gmt file line
    :return: pathway name
    :return: pathway info url
    :return: genes set associated
    """
    name, info, *entries = [
        word.strip()
        for word in line.split('\t')
    ]
    return name, info, {entry.strip() for entry in entries}


def parse_gmt_file(path: Optional[str] = None) -> List[Tuple[str, str, Set[str]]]:
    """Return file as list of pathway - gene sets

    :param path: url from gmt file
    :return: line-based processed file
    """
    with open(path or GMT_HGNC_PATH) as file:
        return [
            _process_line(line)
            for line in file
        ]

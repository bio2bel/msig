# -*- coding: utf-8 -*-

from .constants import GENE_SETS_PATH


def _process_line(line):
    """Returns pathway name, url and gene sets associated

    :param str line: gmt file line
    :rtype: str
    :return: pathway name
    :rtype: str
    :return: pathway info url
    :rtype: list[str]
    :return: genes set associated
    """
    processed_line = [
        word.strip()
        for word in line.split('\t')
    ]

    return processed_line[0], processed_line[1], processed_line[2:]


def parse_gmt_file(url=None):
    """Returns file as list of pathway - gene sets

    :param Optional[str] url: url from gmt file
    :return: line-based processed file
    :rtype: list
    """
    pathways = []
    with open(url if url else GENE_SETS_PATH, 'r') as file:
        for line in file:
            pathway_name, url_info, gene_set = _process_line(line)

            pathways.append((pathway_name, url_info, gene_set))

    return pathways

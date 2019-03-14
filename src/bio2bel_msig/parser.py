# -*- coding: utf-8 -*-

"""Parsers for Bio2BEL MSig."""

import logging
import scrapy
from functools import partial
from scrapy.crawler import CrawlerProcess
from typing import Iterable, List, Optional, Set, Tuple

from .constants import GMT_ENTREZ_PATH, GMT_ENTREZ_URL, GMT_HGNC_SYMBOLS_PATH, GMT_HGNC_SYMBOLS_URL

__all__ = [
    'parse_gmt_file',
    'download',
]

logger = logging.getLogger(__name__)

DOWNLOAD_PAIRS = [
    (GMT_ENTREZ_URL, GMT_ENTREZ_PATH),
    (GMT_HGNC_SYMBOLS_URL, GMT_HGNC_SYMBOLS_PATH),
]


class LoginSpider(scrapy.Spider):
    """A Scrapy Spider for downloading GMT files from GSEA."""

    name = 'bio2bel'
    start_urls = ['http://software.broadinstitute.org/gsea/login.jsp']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'j_username': 'cthoyt@gmail.com',
                'j_password': 'password',
            },
            callback=self.after_login,
        )

    def after_login(self, _):
        """Redirect to the Downloads page."""
        yield scrapy.Request('http://software.broadinstitute.org/gsea/downloads.jsp', callback=self.download_file)

    def download_file(self, _):
        """Redirect to the file path and download with a callback."""
        for url, path in DOWNLOAD_PAIRS:
            yield scrapy.Request(url, callback=partial(self.save_gmt, path=path))

    @staticmethod
    def save_gmt(response, *, path):
        """Save the GMT file."""
        with open(path, 'wb') as f:
            f.write(response.body)


def download(force: bool = False) -> None:
    if has_files() and not force:
        return
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(LoginSpider)
    process.start()
    process.join()


def has_files() -> bool:
    return os.path.exists(GMT_ENTREZ_PATH) and os.path.exists(GMT_HGNC_SYMBOLS_PATH)


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
    with open(path or GMT_HGNC_SYMBOLS_PATH) as file:
        return [
            _process_line(line)
            for line in file
        ]

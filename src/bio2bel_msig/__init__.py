# -*- coding: utf-8 -*-

"""
Bio2BEL MSIG is a package for enriching BEL networks with MSIG DB. Furthermore, it is integrated in the `ComPath environment <https://github.com/ComPath>`_ for pathway database comparison.

Citation
--------
- Subramanian, A., Tamayo, P., Mootha, V. K., Mukherjee, S., Ebert, B. L., Gillette, M. A., ... & Mesirov, J. P. (2005). Gene set enrichment analysis: a knowledge-based approach for interpreting genome-wide expression profiles. Proceedings of the National Academy of Sciences, 102(43), 15545-15550.
"""

import logging

from pkg_resources import VersionConflict, iter_entry_points

from .constants import MODULE_NAME

log = logging.getLogger(__name__)

managers = {}

for entry_point in iter_entry_points(group=MODULE_NAME, name=None):
    entry = entry_point.name

    try:
        bio2bel_module = entry_point.load()
    except VersionConflict:
        log.warning('Version conflict in %s', entry)
        continue

    try:
        managers[entry] = bio2bel_module.Manager
    except Exception:
        log.warning('%s does not have a top-level Manager class', entry)
        continue

__version__ = '0.0.1-dev'

__title__ = 'MSIG'
__description__ = "A wrapper around MSIGDB"
__url__ = 'https://github.com/bio2bel/MSIG'

__author__ = 'Daniel Domingo-Fernández and Charles Tapley Hoyt'
__email__ = 'daniel.domingo.fernandez@scai.fraunhofer.de'

__license__ = 'MIT License'
__copyright__ = 'Copyright (c) 2017-2018 Daniel Domingo-Fernández and Charles Tapley Hoyt'

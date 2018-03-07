Bio2BEL MSigDB |build| |coverage| |docs|
========================================
This package allows the enrichment of BEL networks with MSigDB information.
Furthermore, it is integrated in the `ComPath environment <https://github.com/ComPath>`_ for pathway database comparison.

Installation
------------
This code can be installed with :code:`pip3 install git+https://github.com/bio2bel/msig.git`

The package expects you have downloaded the gene sets from MSigDB following the instructions and terms stated in their `website <http://software.broadinstitute.org/gsea/downloads.jsp>`_.
The gene sets in gmt format should placed in /resources. However, feel free to change the directory by modifying the constants module.

Functionalities and Commands
----------------------------
Following, the main functionalities and commands to work with this package:

- Populate local database with MSigDB :code:`python3 -m bio2bel_msig populate`
- Run an admin site for simple querying and exploration :code:`python3 -m bio2bel_msig web` (http://localhost:5000/admin/)
- Export gene sets for programmatic use :code:`python3 -m bio2bel_msig export`

Citation
--------
- Subramanian, A., Tamayo, P., Mootha, V. K., Mukherjee, S., Ebert, B. L., Gillette, M. A., ... & Mesirov, J. P. (2005). Gene set enrichment analysis: a knowledge-based approach for interpreting genome-wide expression profiles. Proceedings of the National Academy of Sciences, 102(43), 15545-15550.

- Liberzon, A., Subramanian, A., Pinchback, R., Thorvaldsdóttir, H., Tamayo, P., & Mesirov, J. P. (2011). Molecular signatures database (MSigDB) 3.0. Bioinformatics, 27(12), 1739-1740.

.. |build| image:: https://travis-ci.org/bio2bel/msig.svg?branch=master
    :target: https://travis-ci.org/bio2bel/msig
    :alt: Build Status

.. |coverage| image:: https://codecov.io/gh/bio2bel/msig/coverage.svg?branch=master
    :target: https://codecov.io/gh/bio2bel/msig?branch=master
    :alt: Coverage Status

.. |docs| image:: http://readthedocs.org/projects/bio2bel-msig/badge/?version=latest
    :target: http://bio2bel.readthedocs.io/projects/msig/en/latest/?badge=latest
    :alt: Documentation Status

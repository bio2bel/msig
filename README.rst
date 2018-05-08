Bio2BEL MSigDB |build| |coverage| |documentation| |zenodo|
==========================================================
This package allows the enrichment of BEL networks with MSigDB information.
Furthermore, it is integrated in the `ComPath environment <https://github.com/ComPath>`_ for pathway database comparison.

Installation |pypi_version| |python_versions| |pypi_license|
------------------------------------------------------------
``bio2bel_msig`` can be installed easily from `PyPI <https://pypi.python.org/pypi/bio2bel_msig>`_ with the
following code in your favorite terminal:

.. code-block:: sh

    $ python3 -m pip install bio2bel_msig

or from the latest code on `GitHub <https://github.com/bio2bel/msig>`_ with:

.. code-block:: sh

    $ python3 -m pip install git+https://github.com/bio2bel/msig.git@master

Setup
-----
The package expects you have downloaded the gene sets from MSigDB following the instructions and terms stated in
their `website <http://software.broadinstitute.org/gsea/downloads.jsp>`_.

The environment variable `BIO2BEL_MSIG_PATH` should be set to the directory where the gene set files in the GMT format
are stored. Optionally, this can be directly overridden with the keyword argument to `populate()` in the REPL or as
a flag in the command line utility.

Python REPL
~~~~~~~~~~~
.. code-block:: python

    >>> import bio2bel_msig
    >>> msig_manager = bio2bel_msig.Manager()
    >>> msig_manager.populate()

Command Line Utility
~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    bio2bel_msig populate

Other Command Line Utilities
----------------------------
- Run an admin site for simple querying and exploration :code:`python3 -m bio2bel_msig web` (http://localhost:5000/admin/)
- Export gene sets for programmatic use :code:`python3 -m bio2bel_msig export`

Citation
--------
- Subramanian, A., *et al.* (2005). Gene set enrichment analysis: a knowledge-based approach for interpreting genome-wide expression profiles. Proceedings of the National Academy of Sciences, 102(43), 15545-15550.
- Liberzon, A., *et al* (2011). Molecular signatures database (MSigDB) 3.0. Bioinformatics, 27(12), 1739-1740.

.. |build| image:: https://travis-ci.org/bio2bel/msig.svg?branch=master
    :target: https://travis-ci.org/bio2bel/msig
    :alt: Build Status

.. |coverage| image:: https://codecov.io/gh/bio2bel/msig/coverage.svg?branch=master
    :target: https://codecov.io/gh/bio2bel/msig?branch=master
    :alt: Coverage Status

.. |documentation| image:: http://readthedocs.org/projects/bio2bel-msig/badge/?version=latest
    :target: http://bio2bel.readthedocs.io/projects/msig/en/latest/?badge=latest
    :alt: Documentation Status

.. |climate| image:: https://codeclimate.com/github/bio2bel/msig/badges/gpa.svg
    :target: https://codeclimate.com/github/bio2bel/msig
    :alt: Code Climate

.. |python_versions| image:: https://img.shields.io/pypi/pyversions/bio2bel_msig.svg
    :alt: Stable Supported Python Versions

.. |pypi_version| image:: https://img.shields.io/pypi/v/bio2bel_msig.svg
    :alt: Current version on PyPI

.. |pypi_license| image:: https://img.shields.io/pypi/l/bio2bel_msig.svg
    :alt: MIT License

.. |zenodo| image:: https://zenodo.org/badge/123948554.svg
    :target: https://zenodo.org/badge/latestdoi/123948554
# -*- coding: utf-8 -*-

"""Testing constants for Bio2BEL MSig."""

import os
import tempfile
import unittest

from bio2bel_msig.manager import Manager
from bio2bel_msig.parser import parse_gmt_file

dir_path = os.path.dirname(os.path.realpath(__file__))
resources_path = os.path.join(dir_path, 'resources')
gene_sets_path = os.path.join(resources_path, 'test_gmt_file.gmt')


class DatabaseMixin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create temporary file."""
        cls.fd, cls.path = tempfile.mkstemp()
        cls.connection = 'sqlite:///' + cls.path

        # create temporary database
        cls.manager = Manager(cls.connection)
        cls.manager.populate(path=gene_sets_path)

    @classmethod
    def tearDownClass(cls):
        """Close the connection in the manager and delete the temporary database."""
        cls.manager.drop_all()
        cls.manager.session.close()
        os.close(cls.fd)
        os.remove(cls.path)

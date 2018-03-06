# -*- coding: utf-8 -*-
""" This module contains all test constants"""

import os
import tempfile
import unittest

from bio2bel_msig.manager import Manager

dir_path = os.path.dirname(os.path.realpath(__file__))
resources_path = os.path.join(dir_path, 'resources')

gene_sets_path = os.path.join(resources_path, 'test_gmt_file.gmt')


class DatabaseMixin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create temporary file"""

        cls.fd, cls.path = tempfile.mkstemp()
        cls.connection = 'sqlite:///' + cls.path

        # create temporary database
        cls.manager = Manager(cls.connection)

        # fill temporary database with test data
        cls.manager.populate(
            path=gene_sets_path
        )

    @classmethod
    def tearDownClass(cls):
        """Closes the connection in the manager and deletes the temporary database"""
        cls.manager.drop_all()
        cls.manager.session.close()
        os.close(cls.fd)
        os.remove(cls.path)

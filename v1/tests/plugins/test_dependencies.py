# -*- coding: utf-8 -*-
from shutil import which
import unittest
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import opulence.common.plugins.dependencies as dep
from opulence.common.plugins.exceptions import BinaryDependencyMissing
from opulence.common.plugins.exceptions import DependencyMissing
from opulence.common.plugins.exceptions import FileDependencyMissing
from opulence.common.plugins.exceptions import ModuleDependencyMissing


class TestPluginDependencies(unittest.TestCase):
    def test_incorect_base_dependency(self):
        d = dep.Dependency("test")
        with self.assertRaises(NotImplementedError) as context:
            d.verify()

    def test_binary_dep_ok(self):
        with patch("opulence.common.plugins.dependencies.which") as mock:
            mock.return_value = "ok"
            d = dep.BinaryDependency("test")
            d.verify()
            mock.assert_called_with("test")

    def test_binary_dep_raises(self):
        with patch("opulence.common.plugins.dependencies.which") as mock:
            mock.return_value = None
            d = dep.BinaryDependency("test")
            with self.assertRaises(BinaryDependencyMissing) as context:
                d.verify()
            mock.assert_called_with("test")

    def test_module_dep_ok(self):
        with patch("opulence.common.plugins.dependencies.import_module") as mock:
            mock.return_value = "ok"
            d = dep.ModuleDependency("mockedimport")
            d.verify()
            d.satisfied()
            mock.assert_called_with("mockedimport")

    def test_module_dep_ok_2(self):
        d = dep.ModuleDependency("unittest")
        d.verify()
        d.satisfied()

    def test_module_dep_raises(self):
        with patch("opulence.common.plugins.dependencies.import_module") as mock:
            mock.side_effect = NotImplementedError
            d = dep.ModuleDependency("mockedimport")
            with self.assertRaises(ModuleDependencyMissing) as context:
                d.verify()

    def test_file_dep_ok(self):
        with patch(
            "opulence.common.plugins.dependencies.os.path.isfile",
        ) as mock_isfile, patch(
            "opulence.common.plugins.dependencies.os.path.exists",
        ) as mock_exists:
            mock_isfile.return_value = True
            mock_exists.return_value = True
            d = dep.FileDependency("mockedfile")
            d.verify()
            d.satisfied()
            mock_isfile.assert_called_with("mockedfile")
            mock_exists.assert_called_with("mockedfile")

    def test_file_raises(self):
        with patch(
            "opulence.common.plugins.dependencies.os.path.isfile",
        ) as mock_isfile, patch(
            "opulence.common.plugins.dependencies.os.path.exists",
        ) as mock_exists:
            mock_isfile.return_value = False
            mock_exists.return_value = True
            d = dep.FileDependency("mockedfile")
            with self.assertRaises(FileDependencyMissing) as context:
                d.verify()
            mock_exists.assert_called_with("mockedfile")
            mock_isfile.assert_called_with("mockedfile")

    def test_file_raises_2(self):
        with patch(
            "opulence.common.plugins.dependencies.os.path.isfile",
        ) as mock_isfile, patch(
            "opulence.common.plugins.dependencies.os.path.exists",
        ) as mock_exists:
            mock_isfile.return_value = False
            mock_exists.return_value = False
            d = dep.FileDependency("mockedfile")
            with self.assertRaises(FileDependencyMissing) as context:
                d.verify()
            mock_exists.assert_called_with("mockedfile")

    def test_file_raises_3(self):
        with patch(
            "opulence.common.plugins.dependencies.os.path.isfile",
        ) as mock_isfile, patch(
            "opulence.common.plugins.dependencies.os.path.exists",
        ) as mock_exists:
            mock_isfile.return_value = True
            mock_exists.return_value = False
            d = dep.FileDependency("mockedfile")
            with self.assertRaises(FileDependencyMissing) as context:
                d.verify()
            mock_exists.assert_called_with("mockedfile")

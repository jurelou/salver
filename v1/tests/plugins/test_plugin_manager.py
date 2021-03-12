from inspect import isclass
import unittest
from unittest.mock import MagicMock
from unittest.mock import call
from unittest.mock import patch

from opulence.common.plugins import BasePlugin
from opulence.common.plugins import PluginManager
from opulence.common.plugins import PluginStatus
from opulence.common.plugins.exceptions import DependencyMissing
from opulence.common.plugins.exceptions import ModuleDependencyMissing
from opulence.common.plugins.exceptions import PluginVerifyError


class basePlugin(BasePlugin):
    _name_ = "name"
    _description_ = "desc"
    _author_ = "author"
    _version_ = 1


class TestPluginManager(unittest.TestCase):
    @patch("opulence.common.plugins.PluginManager")
    def test_plugin_manager_empty(self, mock):
        pm = PluginManager()

        pm._plugins_ = {"test.a": basePlugin(), "test.b": basePlugin()}

        plugins_inst = pm.get_plugins()
        plugins = pm.get_plugins(instance=False)
        plugins_from_pkg = pm.get_plugins(package="test.", instance=False)
        self.assertEqual(len(plugins), 2)
        self.assertEqual(len(plugins_inst), 2)
        self.assertEqual(len(plugins_from_pkg), 2)

    @patch("opulence.common.plugins.basePlugin.issubclass")
    @patch("opulence.common.plugins.basePlugin.inspect.getmembers")
    @patch("opulence.common.plugins.basePlugin.import_module")
    @patch("opulence.common.plugins.basePlugin.pkgutil.iter_modules")
    def test_plugin_manager_discover(
        self, mock_iter_modules, mock_import_module, mock_get_members, mock_is_subclass,
    ):
        def gen_iter_modules():
            yield ("loader", "directory", "ispkg")

        mock_iter_modules.return_value = gen_iter_modules()
        mock_get_members.return_value = []
        mock_import_module.return_value = "module"
        pm = PluginManager()
        pm.discover(".path.to.collector")

        mock_get_members.assert_called_with("module", isclass)
        mock_import_module.assert_called_with(".path.to.collector.directory")
        mock_iter_modules.assert_has_calls(
            [call(["/path/to/collector"]), call(["/path/to/collector/directory"])],
        )

    def test_register(self):
        mock_dependency = MagicMock()
        mock_dependency.verify = MagicMock()

        class basePlugin(BasePlugin):
            _name_ = "name"
            _description_ = "desc"
            _author_ = "author"
            _version_ = 1

            _dependencies_ = [mock_dependency]

            def __init__(self):
                PluginManager().register_plugin(self)

        pm = PluginManager()
        pm._plugins_ = {}
        bp = basePlugin()
        self.assertEqual(len(pm.get_plugins()), 1)
        mock_dependency.verify.assert_called_once()

    def test_plugin_dependency_raises(self):
        mock_dependency = MagicMock()
        mock_dependency.verify = MagicMock()
        mock_dependency.verify.side_effect = ModuleDependencyMissing

        class basePlugin(BasePlugin):
            _name_ = "name"
            _description_ = "desc"
            _author_ = "author"
            _version_ = 1

            _dependencies_ = [mock_dependency]

            def __init__(self):
                PluginManager().register_plugin(self)

        pm = PluginManager()
        pm._plugins_ = {}
        bp = basePlugin()
        mock_dependency.verify.assert_called_once()

    def test_verify_plugin_ok(self):
        mock_dependency = MagicMock()
        mock_dependency.verify = MagicMock()

        class basePlugin(BasePlugin):
            _name_ = "name"
            _description_ = "desc"
            _author_ = "author"
            _version_ = 1

            _dependencies_ = [mock_dependency]

            def __init__(self):
                PluginManager().register_plugin(self)

            verify = MagicMock()

        pm = PluginManager()
        pm._plugins_ = {}
        bp = basePlugin()
        mock_dependency.verify.assert_called_once()
        bp.verify.assert_called_once()
        self.assertEqual(bp.status[0], PluginStatus.READY)

    def test_verify_plugin_raises(self):
        mock_dependency = MagicMock()
        mock_dependency.verify = MagicMock()

        class basePlugin(BasePlugin):
            _name_ = "name"
            _description_ = "desc"
            _author_ = "author"
            _version_ = 1

            _dependencies_ = [mock_dependency]

            def __init__(self):
                PluginManager().register_plugin(self)

            verify = MagicMock()
            verify.side_effect = PluginVerifyError

        pm = PluginManager()
        pm._plugins_ = {}
        bp = basePlugin()
        mock_dependency.verify.assert_called_once()
        bp.verify.assert_called_once()
        self.assertEqual(bp.status[0], PluginStatus.ERROR)

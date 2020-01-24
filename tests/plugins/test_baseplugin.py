import unittest

from opulence.common.plugins import BasePlugin, PluginStatus


class TestBasePlugin(unittest.TestCase):
    def test_simple_base_plugin(self):
        class basePlugin(BasePlugin):
            _name_ = "name"
            _description_ = "desc"
            _author_ = "author"
            _version_ = 1

        bp = basePlugin()
        bp_code, bp_error = bp.status
        self.assertFalse(bp.errored)
        self.assertEqual(bp_error, "")
        self.assertEqual(bp_code, PluginStatus.READY)

        bp_info = bp.get_info()
        self.assertTrue("name" in bp_info["plugin_data"])

    def test_base_plugin_no_name(self):
        class basePlugin(BasePlugin):
            _description_ = "desc"
            _author_ = "author"
            _version_ = 1

        bp = basePlugin()
        bp_code, bp_error = bp.status
        self.assertTrue(bp.errored)
        self.assertTrue("Incorrect plugin_name" in bp_error)
        self.assertEqual(bp_code, PluginStatus.ERROR)
        self.assertTrue(bp.plugin_name.startswith("UNDEFINED-"))

    def test_base_plugin_no_desc(self):
        class basePlugin(BasePlugin):
            _name_ = "name"
            _author_ = "author"
            _version_ = 1

        bp = basePlugin()
        bp_code, bp_error = bp.status
        self.assertTrue(bp.errored)
        self.assertTrue("Incorrect plugin_description" in bp_error)
        self.assertEqual(bp_code, PluginStatus.ERROR)

    def test_base_plugin_no_author(self):
        class basePlugin(BasePlugin):
            _name_ = "name"
            _description_ = "desc"
            _version_ = 1

        bp = basePlugin()
        bp_code, bp_error = bp.status
        self.assertTrue(bp.errored)
        self.assertTrue("Incorrect plugin_author" in bp_error)
        self.assertEqual(bp_code, PluginStatus.ERROR)

    def test_base_plugin_no_author(self):
        class basePlugin(BasePlugin):
            _name_ = "name"
            _description_ = "desc"
            _author_ = "author"

        bp = basePlugin()
        bp_code, bp_error = bp.status
        self.assertTrue(bp.errored)
        self.assertTrue("Incorrect plugin_version" in bp_error)
        self.assertEqual(bp_code, PluginStatus.ERROR)

    def test_base_plugin_wrong_status(self):
        class basePlugin(BasePlugin):
            _name_ = "name"
            _description_ = "desc"
            _author_ = "author"
            _version_ = 1

        bp = basePlugin()
        bp.status = PluginStatus.ERROR

        bp_code, bp_error = bp.status
        self.assertTrue(bp.errored)
        self.assertTrue("Wrong status arguments" in bp_error)
        self.assertEqual(bp_code, PluginStatus.ERROR)

import unittest

from opulence.collectors import app
from opulence.common.plugins import PluginStatus
from opulence.facts import Person


class TestApp(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    # def test_reload_collectors(self):
    #     collectors = app.list_collectors()
    #     self.assertTrue("dummy collector" in collectors)
    #     app.available_collectors = {}
    #     self.assertFalse("dummy collector" in app.available_collectors)
    #     app.reload_collectors(flush=True)
    #     self.assertTrue("dummy collector" in app.available_collectors)
    #     collectors = app.list_collectors()
    #     self.assertTrue("dummy collector" in collectors)

    #     def test_dummy_info_from_app(self):
    #         dummy_info = app.collector_info("dummy collector")
    #         should_be = {
    #             "plugin_data": {
    #                 "name": "dummy collector",
    #                 "version": "1",
    #                 "author": "Louis",
    #                 "category": "BaseCollector",
    #                 "description": "This is an example collector",
    #                 "status": PluginStatus.READY,
    #                 "error": "",
    #                 "canonical_name": "opulence.collectors.collectors.dummy.Dummy",
    #             },
    #             "active_scanning": False,
    #             "allowed_input": [Person().get_info()],
    #         }
    #         self.assertEqual(dummy_info, should_be)

    # def test_dummy_collector_exec_from_app(self):
    #     john = Person(firstname="john", lastname="snow")
    #     res = app.execute_collector_by_name("dummy collector", john)
    #     output = res.output[0]

    #     self.assertEqual(output.firstname.value, "johnDUMMY")
    #     self.assertEqual(output.lastname.value, "snowDUMMY")

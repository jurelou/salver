import unittest

from opulence.common.timer import Clock


class TestStringField(unittest.TestCase):
    def test_started_clock(self):
        c = Clock()
        self.assertFalse(c.started)
        c.start()
        self.assertTrue(c.started)
        c.stop()
        self.assertFalse(c.started)

    def test_time_elapsed(self):
        c = Clock()
        c.start()
        now = c.time_elapsed
        future = c.time_elapsed
        self.assertGreaterEqual(future, now)

    def test_time_elapsed_ended_timer(self):
        c = Clock()
        c.start()
        now = c.time_elapsed
        c.stop()
        future = c.time_elapsed
        self.assertGreaterEqual(future, now)

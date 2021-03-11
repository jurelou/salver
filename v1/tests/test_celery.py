import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from celery.exceptions import TimeoutError

from opulence.common.celery.exceptions import TaskError
from opulence.common.celery.exceptions import TaskTimeoutError
from opulence.common.celery.taskRouter import TaskRouter
from opulence.common.celery.utils import async_call
from opulence.common.celery.utils import sync_call


class TestCeleryTaskRouter(unittest.TestCase):
    def test_simple_router(self):
        tr = TaskRouter()
        res = tr.route_for_task("app:path")
        expected = "{'queue': 'app'}"
        self.assertEqual(str(res), expected)

    def test_simple_router2(self):
        tr = TaskRouter()
        res = tr.route_for_task("app")
        expected = "{'queue': 'default'}"
        self.assertEqual(str(res), expected)


class TestCeleryUtils(unittest.TestCase):
    def test_sync_call_raises(self):
        app = MagicMock()
        app.send_task.side_effect = TimeoutError("timeout")
        with self.assertRaises(TaskTimeoutError) as context:
            sync_call(app, "path!", "timeout")
        expected = "Task timeout: (path!)"
        self.assertEqual(str(context.exception), expected)

    def test_sync_call(self):
        app = MagicMock()
        path, timeout, karg = "path", "timeout", "kwargs"

        expected = ("this", "is", "sparta")
        args = (("%s" % (path),), {"karg": karg})
        app.send_task().get.return_value = expected

        result = sync_call(app, path, timeout, karg=karg)
        self.assertEqual(result, expected)
        self.assertEqual(app.send_task.call_args, args)
        self.assertEqual(app.send_task().get.call_args, (tuple(), {"timeout": timeout}))

    def test004_async_call_ok(self):
        app = MagicMock()
        path, karg = "path", "kwargs"
        expected = ("a", "b")
        args = (("%s" % (path),), {"karg": karg})
        app.send_task.return_value = expected
        result = async_call(app, path, karg=karg)
        self.assertEqual(result, expected)
        self.assertEqual(app.send_task.call_args, args)

    def test_async_call_raises(self):
        app = MagicMock()
        app.send_task.side_effect = TimeoutError("timeout")
        with self.assertRaises(TaskTimeoutError) as context:
            async_call(app, "path!")
        expected = "Task timeout: (path!)"
        self.assertEqual(str(context.exception), expected)

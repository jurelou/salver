import unittest
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

from opulence.common import configuration


class TestConfig(unittest.TestCase):
    def test_empty_conf(self):
        with patch("opulence.common.configuration.Celery") as mock_celery:
            celery_obj = Mock()
            celery_obj.return_value = "celery mock"
            celery_obj.conf.update = MagicMock()
            mock_celery.return_value = celery_obj

            base_return = {
                "task_routes": ("opulence.common.celery.taskRouter.TaskRouter",),
                "accept_content": ["customEncoder", "application/json"],
                "task_serializer": "customEncoder",
                "result_serializer": "customEncoder",
            }

            app = configuration.configure_celery({})

            celery_obj.conf.update.assert_called_with(base_return)

    def test_conf(self):
        with patch("opulence.common.configuration.Celery") as mock_celery, patch(
            "opulence.common.configuration.register",
        ) as mock_register:
            celery_obj = Mock()
            celery_obj.return_value = "celery mock"
            celery_obj.conf.update = MagicMock()
            mock_celery.return_value = celery_obj

            base_return = {
                "task_routes": ("opulence.common.celery.taskRouter.TaskRouter",),
                "accept_content": ["customEncoder", "application/json"],
                "task_serializer": "customEncoder",
                "result_serializer": "customEncoder",
            }
            additional_return = {"a": "bb", "c": 42}
            base_return.update(additional_return)
            app = configuration.configure_celery(additional_return)
            celery_obj.conf.update.assert_called_with(base_return)
            mock_register.assert_called_once()

    def test_conf(self):
        with patch("opulence.common.configuration.Celery") as mock_celery, patch(
            "opulence.common.configuration.register",
        ) as mock_register:
            celery_obj = Mock()
            celery_obj.return_value = "celery mock"
            celery_obj.conf.update = MagicMock()
            mock_celery.return_value = celery_obj

            app = configuration.configure_celery({}, custom_encoder=False)
            mock_register.assert_not_called()

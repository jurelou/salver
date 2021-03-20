# -*- coding: utf-8 -*-
from opulence.engine.tasks import launch_scan


def test_some_task(celery_app):
    # launch_scan.s(1).apply()
    pass



# -*- coding: utf-8 -*-
from opulence.engine.database.manager import DatabaseManager
from opulence.common import models
import pytest
from uuid import uuid4
from opulence.facts.username import Username
from opulence.engine.database import exceptions

@pytest.mark.usefixtures("database_manager")
class TestDatabaseManager:
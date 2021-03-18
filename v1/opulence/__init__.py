# -*- coding: utf-8 -*-
from dynaconf import settings

from opulence.common.configuration import configure_celery

App = configure_celery(settings.CELERY_BROKER)

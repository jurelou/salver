# -*- coding: utf-8 -*-
from loguru import logger

from salver.common import models
from salver.common.kafka import ConsumerCallback
from salver.engine.services.mongodb import get_database, add_new_collect


class OnCollectCreate(ConsumerCallback):
    def __init__(self):
        self.db = get_database()

    def on_message(self, collect: models.Collect):
        add_new_collect(self.db, collect)

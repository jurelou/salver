# -*- coding: utf-8 -*-
from salver.config import api_config
from salver.common.database import DatabaseManager

db_manager = DatabaseManager(
    neo4j_config=api_config.neo4j,
    elasticsearch_config=api_config.elasticsearch,
    mongodb_config=api_config.mongodb,
)


async def get_database() -> DatabaseManager:
    return db_manager

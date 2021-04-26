# -*- coding: utf-8 -*-
from dynaconf import Dynaconf
from loguru import logger

engine_config = Dynaconf(
    envvar_prefix='DYNACONF',
    settings_files=['salver/engine/settings.yaml'],
    environments=True,
)

agent_config = Dynaconf(
    envvar_prefix='DYNACONF',
    settings_files=['salver/agent/settings.yaml'],
    environments=True,
)

# api_config = Dynaconf(
#     envvar_prefix='DYNACONF',
#     settings_files=['salver/api/settings.yaml'],
#     environments=True,
# )

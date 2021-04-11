# -*- coding: utf-8 -*-
from dynaconf import Dynaconf

controller_config = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=["salver/controller/settings.yaml"],
    environments=True,
)

agent_config = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=["salver/agent/settings.yaml"],
    environments=True,
)

api_config = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=["salver/api/settings.yaml"],
    environments=True,
)

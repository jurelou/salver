from dynaconf import Dynaconf

engine_config = Dynaconf(
    envvar_prefix="DYNACONF", settings_files=["opulence/engine/settings.yaml"],
)

agent_config = Dynaconf(
    envvar_prefix="DYNACONF", settings_files=["opulence/agent/settings.yaml"],
)

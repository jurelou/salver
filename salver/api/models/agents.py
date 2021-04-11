from typing import List

from pydantic import BaseModel

from salver.controller.models import Agent


class AgentInResponse(BaseModel):
    agent: Agent


class AgentsInResponse(BaseModel):
    agents: List[Agent]

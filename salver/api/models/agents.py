from salver.controller.models import Agent
from pydantic import BaseModel

from typing import List

class AgentInResponse(BaseModel):
    agent: Agent

class AgentsInResponse(BaseModel):
    agents: List[Agent]
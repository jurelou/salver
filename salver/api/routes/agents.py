# -*- coding: utf-8 -*-
from fastapi import APIRouter, HTTPException

from salver.api.models.agents import AgentInResponse, AgentsInResponse
from salver.api.services.remote_tasks import sync_call, async_call

router = APIRouter()


@router.get("/", response_model=AgentsInResponse)
async def get_agents():
    agents = sync_call("salver.controller.tasks.list_agents")
    return AgentsInResponse(agents=agents)


@router.get("/reload")
async def reload_agents():
    async_call("salver.controller.tasks.reload_agents")
    return "ok"


@router.get("/{agent_name}", response_model=AgentInResponse)
async def get_agent(agent_name):
    agents = sync_call("salver.controller.tasks.list_agents")
    for agent in agents:
        if agent.name == agent_name:
            return AgentInResponse(agent=agent)
    raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")

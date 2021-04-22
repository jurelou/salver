# -*- coding: utf-8 -*-
from fastapi.testclient import TestClient
from salver.api.main import app

from mock import patch

client = TestClient(app)


class TestAgents:
    def test_get_agents(self):
        res = client.get('/api/agents')
        assert res.status_code == 200

        agents = res.json()['agents']
        assert len(agents) == 1

        collectors = agents[0]['collectors']
        assert any(
            [
                c
                for c in collectors
                if c['config']['name'] == 'dummy-collector' and c['active']
            ],
        )

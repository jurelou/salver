# -*- coding: utf-8 -*-
from fastapi.testclient import TestClient
from salver.api.main import app

client = TestClient(app)


def create_case(case, **kwargs):
    res = client.post('/api/cases/', data=case.json())
    return __check_response(res, **kwargs)


def get_case(case_id, **kwargs):
    res = client.get(f'/api/cases/{case_id}')
    return __check_response(res, **kwargs)


def get_scan(scan_id, **kwargs):
    res = client.get(f'/api/scans/{scan_id}')
    return __check_response(res, **kwargs)


def get_all_cases(**kwargs):
    res = client.get(f'/api/cases')
    return __check_response(res, **kwargs)


def get_all_scans(**kwargs):
    res = client.get(f'/api/scans')
    return __check_response(res, **kwargs)

def launch_scan(scan_id, **kwargs):
    res = client.get(f'/api/scans/{scan_id}/launch')
    return __check_response(res, **kwargs)


def create_scan(scan, **kwargs):
    res = client.post('/api/scans/', data=scan.json())
    return __check_response(res, **kwargs)


def __check_response(response, check_200=True, get_return_code=False, **kwargs):
    if check_200:
        if response.status_code not in (200, 201):
            print(f'Error: {response.status_code}: {response.text}')
        assert response.status_code in (200, 201)
    try:
        content = response.json()
    except Exception:
        content = response.text

    if get_return_code:
        return response.status_code, content
    return content

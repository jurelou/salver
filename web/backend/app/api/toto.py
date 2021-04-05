# -*- coding: utf-8 -*-
from fastapi import APIRouter, WebSocket

router = APIRouter()


@router.get("/toto")
async def test_toto():
    return "toto works wellaa"


@router.websocket("/ws")
async def test_ws(websocket: WebSocket):
    print("!!!!!!!!!!!")
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

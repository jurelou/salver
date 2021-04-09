# -*- coding: utf-8 -*-
from fastapi import APIRouter, WebSocket
from app.services.remote_tasks import sync_call
router = APIRouter()




@router.get("/toto")
async def test_toto():
    #remote_tasks.async_call(
    #         "salver.controller.tasks.ping",
    #         )
    t = sync_call("salver.controller.tasks.ping" )
    return f"toto works wellaaaaaaaaa {t}"


@router.websocket("/ws")
async def test_ws(websocket: WebSocket):
    print("!!!!!!!!!!!")
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

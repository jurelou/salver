# -*- coding: utf-8 -*-
import socketio

from salver.config import api_config

sio = socketio.AsyncServer(
    async_mode="asgi", cors_allowed_origins=[], logger=True, engineio_logger=True,
)
socket_app = socketio.ASGIApp(sio)


@sio.on("disconnect")
def test_disconnect(sid):
    print("Client disconnectedaaaaaaaaaaaaaa")


@sio.on("connect")
async def connect(sid, environ):
    print("!!!!!!!!!!!!!!connectedaaaaaaaaa", sid)
    await sio.emit("tofront", "salutlol")


@sio.on("chat")
def connecazet(*args, **kwargs):
    print("!!!!!!!!!!!!!!chattttttt", "sid")

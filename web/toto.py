# -*- coding: utf-8 -*-

import socketio

sio = socketio.Client()


@sio.event
def connect():
    print("connection established")


@sio.event
def my_message(data):
    print("message received with ", data)
    sio.emit("my response", {"response": "my response"})


@sio.event
def disconnect():
    print("disconnected from server")


sio.connect("http://127.0.0.1:8000/subapi/")
sio.wait()

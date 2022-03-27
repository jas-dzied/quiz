#!/usr/bin/env python3

import time
import threading

def looper():
    counter = 0
    while True:
        counter += 1
        print(f'loop: {counter}')
        time.sleep(1)



loop = threading.Thread(target=looper)
loop.start()

import asyncio
import websockets
import json

async def recv_event(socket, event_type):
    response_type = None
    while response_type != event_type:
        response = await socket.recv()
        respone_type = response["type"]
    return response

async def test():
    async with websockets.connect("ws://localhost:8001") as websocket:

        await websocket.send(json.dumps({
            "type": "join",
            "username": input('Username: ')
        }))
        response = json.loads(await websocket.recv())
        uid = response["uid"]
        is_host = response["host"]

        while True:

            if is_host:

                choice = input("action? (0 see players, 1 start) ")

                if choice == "0":
                    await websocket.send(json.dumps({
                        "type": "list"
                    }))
                    response = json.loads(await websocket.recv())
                    [print(player) for player in response["data"]]

            else:

                event = json.loads(await websocket.recv())
                if event["type"] == "joined":
                    print(f"New player joined: {event['username']}")

main = threading.Thread(target=lambda: asyncio.run(test()))
main.start()

loop.join()
main.join()

#!/usr/bin/env python3

import asyncio
import websockets
import threading
import queue
import secrets

async def worker(uid, q):
    async with websockets.connect("ws://localhost:8003") as websocket:
        await websocket.send(f'0:{uid}')

async def receiver(uid, q):
    async with websockets.connect("ws://localhost:8003") as websocket:
        await websocket.send(f'1:{uid}')

def watcher_starter(*args):
    asyncio.run(worker(*args))
def sender_starter(*args):
    asyncio.run(receiver(*args))

async def main():

    uid = secrets.token_urlsafe(16)
    print(f'My uid: {uid}')

    q = queue.Queue()
    watcher_thread = threading.Thread(target=watcher_starter, args=(uid,q))
    sender_thread = threading.Thread(target=sender_starter, args=(uid,q))
    watcher_thread.start()
    sender_thread.start()
    watcher_thread.join()
    sender_thread.join()

asyncio.run(main())

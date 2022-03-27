#!/usr/bin/env python3

import asyncio
import websockets

users = set()

async def handler(websocket):
    global users

    try:
        users.add(websocket)
        async for message in websocket:
            await websockets.broadcast(users, message)
    finally:
        users.remove(websocket)

async def main():
    async with websockets.serve(handler, "localhost", 8001):
        await asyncio.Future()

asyncio.run(main())

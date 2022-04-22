#!/usr/bin/env python3

import asyncio
import websockets
import json

users = []

async def handler(websocket):

    global users

    try:
        async for message in websocket:
            print(message)
    finally:
        users.remove(websocket)

async def main():
    async with websockets.serve(handler, port=42069):
        await asyncio.Future()

asyncio.run(main())

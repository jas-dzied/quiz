#!/usr/bin/env python3

import asyncio
import websockets
import json

def create_event(name, data={}):
    return json.dumps({
        'event': name,
        **data
    })

class PlayerInfo:
    def __init__(self, socket, username):
        self.socket = socket
        self.username = username
        self.points = 0
        self.previous = None

class SocketServer:
    def __init__(self):
        self.connected = []
        self.players = []
        self.host = None
        self.questions = [
            {
                "text": "What is the capital of England?",
                "options": ["London", "Paris", "Spain"]
            },
            {
                "text": "Yes or no?",
                "options": ["Yes", "No"]
            }
        ]
        self.answers = [
            "London",
            "Yes"
        ]
        self.question_index = 0

    async def send_host(self, event):
        await self.host.send(event)
    async def send_players(self, event):
        for player in self.players:
            await player.socket.send(event)
    def get_player(self, socket):
        for player in self.players:
            if player.socket == socket:
                return player

    async def send_question(self):
        await self.send_players(create_event("question", self.questions[self.question_index]))
        await self.send_host(create_event("host_question"))
        self.question_index += 1

    async def handle_host(self, websocket):
        try:
            self.connected.append(websocket)
            print(f'Host {id(websocket)} connected')
            await websocket.send(create_event("host"))
            async for event in websocket:
                message = json.loads(event)

                if message["event"] == "start":
                    print("Game starting")
                    await self.send_host(create_event("delete_class", {"cls": 1}))
                    await self.send_players(create_event("delete_class", {"cls": 1}))
                    await self.send_question()
                elif message["event"] == "next_question":
                    if self.question_index < len(self.questions):
                        await self.send_players(create_event("leaderboard", {
                            "players": {player.username: player.points for player in self.players}
                        }))
                        await asyncio.sleep(5)
                        await self.send_question()
                    else:
                        await self.send_players(create_event("leaderboard", {
                            "players": {player.username: player.points for player in self.players}
                        }))
                        evt = create_event("end")
                        await self.send_players(evt)
                        await self.send_host(evt)

        finally:
            self.connected.remove(websocket)
            print(f'Host {id(websocket)} disconnected')

    async def handle_player(self, websocket):
        try:
            self.connected.append(websocket)
            print(f'Websocket {id(websocket)} connected')
            await websocket.send(create_event("request_username"))
            async for event in websocket:
                message = json.loads(event)

                if message["event"] == "username":
                    print(f'Player {message["username"]} joined.')
                    self.players.append(PlayerInfo(websocket, message["username"]))
                    await self.send_host(create_event("player_joined", {"username": message["username"]}))
                elif message["event"] == "answer":
                    player = self.get_player(websocket)
                    print(f'Player {player.username} chose {message["choice"]}')
                    await self.send_host(create_event("player_answered", {"username": player.username}))
                    if message["choice"] == self.answers[self.question_index-1]:
                        print('Which is correct.')
                        player.points += 1
                    else:
                        print('Which is wrong.')

        finally:
            self.connected.remove(websocket)
            print(f'Websocket {id(websocket)} disconnected')

    async def handle(self, websocket):
        if self.host is None:
            self.host = websocket
            await self.handle_host(websocket)
        else:
            await self.handle_player(websocket)

async def main():
    server = SocketServer()
    async with websockets.serve(server.handle, port=42069):
        await asyncio.Future()

asyncio.run(main())

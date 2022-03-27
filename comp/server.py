#!/usr/bin/env python3

import asyncio
import websockets
import json

users = []
started = False

async def event_message(websocket, message):
    await websocket.send(json.dumps({
        "event": "message",
        "data": message
    }))

questions = [
    {
        "message": "What is correct?",
        "options": ["wrong1", "correct", "wrong2", "wrong3"],
        "answer": "correct"
    },
    {
        "message": "What is the capital of England",
        "options": ["Madrid", "Paris", "London", "Islamabad"],
        "answer": "London"
    },
    {
        "message": "True or false? England is a country",
        "options": ["True", "False"],
        "answer": "True"
    }
]
question_index = 0

score = {}
answered = {}

async def ask_question():

    global users
    global score
    global answered
    global questions
    global question_index

    for ws in users:
        answered[ws] = False

    try:
        websockets.broadcast(users, json.dumps({
            "event": "question",
            "id": question_index,
            "message": questions[question_index]["message"],
            "options": questions[question_index]["options"]
        }))
    finally:
        websockets.broadcast(users, json.dumps({
            "event": "leaderboard",
            "id": question_index,
            "scores": {f"Player {i}": score[ws] for i, ws in enumerate(score)}
        }))

async def handler(websocket):

    global users
    global started
    global questions
    global question_index
    global score

    try:
        async for message in websocket:

            if started == False:

                if message == "JOIN" and websocket not in users:

                    users.append(websocket)
                    await event_message(websocket, "Joined the lobby.")

                    if len(users) >= 2:

                        websockets.broadcast(users, json.dumps({
                            "event": "start"
                        }))
                        started = True

                        for ws in users:
                            score[ws] = 0
                        await ask_question()

                elif message == "JOIN":
                    await event_message(websocket, "You have already joined the lobby")
                elif websocket in users:
                    print(f"Message received: {message}")
                else:
                    await event_message(websocket, "You are not in the lobby.")

            else:

                if message == "JOIN":
                    await event_message(websocket, "The game has already started.")

                else:
                    event = json.loads(message)
                    if event["event"] == "answer":
                        question = questions[event["qid"]]
                        if event["choice"] == question["answer"]:
                            score[websocket] += 1
                            await event_message(websocket, "Correct!")
                        else:
                            score[websocket] -= 1
                            await event_message(websocket, "Wrong!")
                        answered[websocket] = True

                        if all(answered.values()):
                            question_index += 1
                            await ask_question()


    finally:
        users.remove(websocket)

async def main():
    async with websockets.serve(handler, port=42069):
        await asyncio.Future()

asyncio.run(main())

import asyncio
import json
import logging
import websockets
from datetime import datetime

logging.basicConfig()

USERS = set()

USERNAMES = {0: "Server", -1: ""}


def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})


async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    
    await websocket.send(json.dumps({"type": "message", 
                                    "user": "Server", 
                                     "time": datetime.now().strftime("%H:%M:%S"),
                                     "text": "Wellcome to the server! Please input a valid name"}))
    try:
        async for message in websocket:
            data = json.loads(message)
            if data["type"] == "message":
                if data["text"] not in USERNAMES.values(): 
                    USERNAMES[websocket] = data["text"]
                    await websocket.send(json.dumps({"type": "message", 
                                                     "user": "Server", 
                                                     "time": datetime.now().strftime("%H:%M:%S"),
                                                     "text": "Valid name!",
                                                     "name": data["text"]}))
                    notifMessage = json.dumps({"type": "message", 
                                               "user": "Server", 
                                               "time": datetime.now().strftime("%H:%M:%S"),
                                               "text": "New user:" + data["text"]}) 
                    USERS.add(websocket)
                    await notify_users()
                    await asyncio.wait([user.send(notifMessage) for user in USERS])
                    break
                else:
                    await websocket.send(json.dumps({"type": "message", 
                                                     "user": "Server", 
                                                     "time": datetime.now().strftime("%H:%M:%S"),
                                                     "text": "Invalid name! Try again"}))
            else:
                logging.error("unsupported event: {}", data)
    finally:
        pass

    


async def unregister(websocket):
    if websocket in USERS:
        USERS.remove(websocket)
        del USERNAMES[websocket]
    await notify_users()


async def chat(websocket, path):
    await register(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            if data["type"] == "message":
                if USERS:
                    await asyncio.wait([user.send(message) for user in USERS])
            else:
                logging.error("unsupported event: {}", data)
    finally:
        await unregister(websocket)


start_server = websockets.serve(chat, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


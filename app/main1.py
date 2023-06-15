from fastapi import FastAPI,Response
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import  user, auth,data, post,postdetails
from .config import settings
 
import asyncio
import logging
from datetime import datetime
# Working code---------------------------------------------
# from fastapi import FastAPI, WebSocket, WebSocketDisconnect

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger("FastAPI app")

app = FastAPI()


# async def heavy_data_processing(data: dict):
#     """Some (fake) heavy data processing logic."""
#     await asyncio.sleep(2)
#     message_processed = data.get("message", "").upper()
#     return message_processed


# # Note that the verb is `websocket` here, not `get`, `post`, etc.
# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     # Accept the connection from a client.
#     await websocket.accept()

#     while True:
#         try:
#             # Receive the JSON data sent by a client.
#             data = await websocket.receive_json()
#             # Some (fake) heavey data processing logic.
#             message_processed = await heavy_data_processing(data)
#             # Send JSON data to the client.
#             await websocket.send_json(
#                 {
#                     "message": message_processed,
#                     "time": datetime.now().strftime("%H:%M:%S"),
#                     # "HI":"HI"
#                 }
#             )
#         except WebSocketDisconnect:
#             logger.info("The connection is closed.")
#             break
#   ----------------------------------------------------
import asyncio
import websockets

connected_clients = set()

async def handle_message(message, websocket):
    for client in connected_clients:
        if client != websocket:
            await client.send(message)

async def handle_websocket(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            await handle_message(message, websocket)
    finally:
        connected_clients.remove(websocket)
        
async def main():
    start_server = websockets.serve(handle_websocket, 'localhost', 8000)
    await start_server

if __name__ == '__main__':
    asyncio.run(main())

origins = ["http://localhost:4200"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



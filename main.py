from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import websockets
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def get():
    with open("static/index.html", "r") as file:
        return HTMLResponse(content=file.read(), status_code=200)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    message_counter = 1
    
    while True:
        # Получение сообщения от клиента
        message = await websocket.receive_text()
        
        # Обработка полученного текста
        processed_message = f"{message_counter}: {message}"
        message_counter += 1
        
        # Отправка обработанного сообщения клиенту
        await websocket.send_text(json.dumps({"text": processed_message}))
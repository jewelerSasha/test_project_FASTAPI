from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Подключаем папку со статическими файлами для отображения веб-страницы.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключаем папку с шаблонами для отображения веб-страницы.
templates = Jinja2Templates(directory="templates")

# Список очереди сообщений
messages = []

@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    counter = 0
    while True:
        data = await websocket.receive_json()
        message = data.get("message")
        counter +=1
        if message:
            messages.append(message)
            response = {"message": message, "number": counter}
            await websocket.send_json(response)
            
@app.get("/messages")
async def get_messages():
    return {"messages": messages}
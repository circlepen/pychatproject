from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from api import routes
from api.manager import ws_manager
from db.database import engine, metadata

metadata.create_all(engine)
app = FastAPI(root_path="/", docs_url="/docs")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_items(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/pick")
async def pick_person(request: Request):
    return templates.TemplateResponse("pickperson.html", {"request": request})

@app.get("/chat")
async def get_chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@app.websocket("/ws")
async def ws_chat(websocket: WebSocket):
    sender = websocket.cookies.get("X-Authorization")
    target = websocket.cookies.get("X-TargetUser")

    if sender:
        if target:
            await ws_manager.connect(websocket, sender, target)
            response = {
                "sender": sender,
                "message": "",
                "action": "got connected"
            }
            await ws_manager.send_personal_message(response, sender, target)
            response["action"] = ""
            try:
                while True:
                    data = await websocket.receive_json()
                    await ws_manager.send_personal_message(data, sender, target)
            except WebSocketDisconnect:
                ws_manager.disconnect(websocket, sender, target)
                response['action'] = "left"
                await ws_manager.send_personal_message(response, sender, target)
        else:
            await ws_manager.connect(websocket, sender)
            response = {
                "sender": sender,
                "message": "",
                "action": "got connected"
            }
            await ws_manager.broadcast(response)
            response["action"] = ""
            try:
                while True:
                    data = await websocket.receive_json()
                    await ws_manager.broadcast(data)
            except WebSocketDisconnect:
                ws_manager.disconnect(websocket, sender)
                response['action'] = "left"
                await ws_manager.broadcast(response)

app.include_router(routes.router, prefix="/api", tags=["api"])

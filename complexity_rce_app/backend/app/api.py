from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI,  Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import uuid

import app.modules.coreLogic as coreLogic

app = FastAPI()

origins = [
    "http://localhost:5173",
    "localhost:5173"
]


app = FastAPI()
executor = ThreadPoolExecutor()
tasks_db = {} 

app.add_middleware(
    SessionMiddleware,
    secret_key="secret_key1234567890", # TODO: Yeah this obviously also shouldn'T go into production
    same_site="none",
    https_only=True, # TODO: REMOVE THIS IN PRODUCTION: HTTPS requirement disabled for local development (different ports)
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/get-session-id/", tags=["session"])
async def get_session_id(request: Request):
    if "session_id" not in request.session:
        #Generate unique session id to keep track of which code and complexity belongs to which user
        request.session["session_id"] = str(uuid.uuid4())
    return {"session_id": request.session["session_id"]}

@app.post("/start-task/", tags=["task"])
async def start_task(session_id: str, data: str):
    task_id = str(uuid.uuid4())
    tasks_db[task_id] = {"session_id": session_id, "status": "pending", "result": None}

    def run_task():
        tasks_db[task_id]["status"] = "completed"
        tasks_db[task_id]["result"] = f"Processed {data} for session {session_id}"

    executor.submit(run_task)
    return {"task_id": task_id, "session_id": session_id}

@app.get("/task-status/{task_id}", tags=["task"])
async def get_task_status(task_id: str, session_id: str):
    task = tasks_db.get(task_id)
    if not task or task["session_id"] != session_id:
        return {"error": "Task not found or unauthorized"}
    return task
from fastapi import FastAPI
from pydantic import BaseModel
from llm import chat, memory_clear, chatcusttomer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

class Message(BaseModel):
    message: str

@app.post("/chat")
async def send_message(data: Message, response_class=None, response_content_type="text/plain"):
    res = chat(data.message)
    return str(res)

@app.post("/new")
async def clear(response_class=None, response_content_type="text/plain"):
    res = memory_clear()
    return res

@app.post("/free")
async def send_messages(data: Message, response_class=None, response_content_type="text/plain"):
    res = chatcusttomer(data.message)
    return str(res)

from fastapi import FastAPI
from pydantic import BaseModel
from llm import chat, memory_clear, chatcusttomer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
@app.post("/test")
async def send_messages(response_class=None, response_content_type="text/plain"):

    return """ Title: Certificates and solemnization of marriages upon alteration of divisions\n Law sections and its subsections related to question: Section 4 ([8, 22 of 1955]), Section 10 ([10, 22 of 1946]), Section 14 ([7, 34 of 1946]) and Section 28 ([7, of 1944])\n Answer: For a marriage certificate to be issued by a district registrar from the old or new division when an area undergoes a transition as outlined in Law [7, of 1944] Section 28, a marriage must be solemnized in pursuance of Section 33 of the law without any of the preliminaries prescribed by Sections 4 and 10. The required acts must be done by a District Registrar of the old division or the new division nominated by the District Registrar within the District, and the Registrar-General must periodically publish a list of Registrars of Marriages in Sri Lanka, and the buildings they administer, as laid down by Section 14 ([7, 34 of 1946]).\n Conclusion: In conclusion, marriage certificates may be issued by a district registrar from the old or new division when an area undergoes a transition as outlined in Law [7, of 1944] Section 28 under the following conditions: a marriage must be solemnized in pursuance of"""

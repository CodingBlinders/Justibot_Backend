from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.prompts.prompt import PromptTemplate
from dotenv import load_dotenv
import os

from promptTemplates import template, template2

load_dotenv()

OPENAI_KEY = os.getenv("apikey")

prompt = PromptTemplate(input_variables=["chat_history", "question", "context"], template=template)
prompt2 = PromptTemplate(input_variables=["chat_history", "question", "context"], template=template2)


embeddings = OpenAIEmbeddings(openai_api_key = OPENAI_KEY)
memory = ConversationBufferMemory(
    memory_key="chat_history",
    ai_prefix="AI Lawyer",
    return_messages=True
)

openai = ChatOpenAI(temperature=1, openai_api_key=OPENAI_KEY, model="gpt-3.5-turbo")
faiss_db = FAISS.load_local("faiss_index", embeddings)



chat_llm = ConversationalRetrievalChain.from_llm(openai, faiss_db.as_retriever(search_kwargs={"k": 8}), memory=memory,combine_docs_chain_kwargs={"prompt": prompt}, verbose=True)
chat_llm2 = ConversationalRetrievalChain.from_llm(openai, faiss_db.as_retriever(search_kwargs={"k": 5}), memory=memory,combine_docs_chain_kwargs={"prompt": prompt2}, verbose=True)


def memory_clear():
    memory.clear()
    return "New Chat Created"
def chat(question):
    chat_history= memory.load_memory_variables({})

    res = chat_llm({"question": question, "chat_history": chat_history})
    # n=0
    # memory.clear()
    memory.save_context({"input": question}, {"output": res['answer']})
    return res['answer']

# create_db("law.pdf")

def chatcusttomer(question):
    chat_history= memory.load_memory_variables({})
    res = chat_llm2({"question": question, "chat_history": chat_history})
    # n=0
    # memory.clear()
    memory.save_context({"input": question}, {"output": res['answer']})
    return res['answer']

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

load_dotenv()

OPENAI_KEY = os.getenv("apikey")

template = """
  You are an AI Lawyer. Conversation between a human and an AI lawyer and related context are given. Use the following pieces of context to answer the question at the end. If question is not related to law, just say that "I cannot Assist with that! It's not related for Law. ", don't try to make up an answer.
  The laws have sections and subsections. A section start with number and sections (ex: "4.") and  also has Law number  (ex: [2, 12 of 1997]) also has subsection with (1), (2) like wise.
  you should follow below template. related data provide in "CONTEXT:"
  ANSWER TEMPLATE:
    [Title]
    [Law sections and its subsections related to question]
    [Answer]
    [Conclusion]
  CONTEXT:
  {context}
  
  QUESTION: 
  {question}

  CHAT HISTORY:
  {chat_history}
  
  ANSWER:
  """

template2 = """
  You are an AI Lawyer. Conversation between a human and an AI lawyer and related context are given. Use the following pieces of context to answer the question at the end. If question is not related to law, just say that "I cannot Assist with that! It's not related for Law. ", don't try to make up an answer.
  you should follow below template. also  related srilanka law data provide in "CONTEXT:" your response is not going to very law technical. so please write with law and explations and describe how to do and answer question and also you give instructions as AI Lawyer
  ANSWER TEMPLATE:
    [Title]
    [Answer]
    [Conclusion]
  CONTEXT:
  {context}

  QUESTION: 
  {question}

  CHAT HISTORY:
  {chat_history}

  ANSWER:
  """

prompt = PromptTemplate(input_variables=["chat_history", "question", "context"], template=template)
prompt2 = PromptTemplate(input_variables=["chat_history", "question", "context"], template=template2)

# define embedding
embeddings = OpenAIEmbeddings(
    openai_api_key = OPENAI_KEY
)
# define memory
memory = ConversationBufferMemory(memory_key="chat_history", ai_prefix="AI Lawyer", return_messages=True)

openai = OpenAI(temperature=1, openai_api_key=OPENAI_KEY)
# memory = ConversationSummaryBufferMemory(llm=openai, max_token_limit=1000)
# db3 = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
faiss_db = FAISS.load_local("faiss_index", embeddings)


# define chain
chat_llm = ConversationalRetrievalChain.from_llm(openai, faiss_db.as_retriever(search_kwargs={"k": 8}), memory=memory,combine_docs_chain_kwargs={"prompt": prompt}, verbose=True)
chat_llm2 = ConversationalRetrievalChain.from_llm(openai, faiss_db.as_retriever(search_kwargs={"k": 5}), memory=memory,combine_docs_chain_kwargs={"prompt": prompt2}, verbose=True)

def create_db(file):
    # load documents
    loader = PyPDFLoader(file)
    documents = loader.load()
    documents = documents[:16]
    # split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=80)
    docs = text_splitter.split_documents(documents)
    db = FAISS.from_documents(docs, embeddings)
    db.save_local("faiss_index")
    # vectordb.persist()

def get_chat_history():
    return memory.load_memory_variables({})
    # return ConversationBufferMemory(memory_key="chat_history", return_messages=True)

def memory_clear():
    memory.clear()
    return "New Chat Created"
def chat(question):
    chat_history= get_chat_history()

    res = chat_llm({"question": question, "chat_history": chat_history})
    # n=0
    # memory.clear()
    memory.save_context({"input": question}, {"output": res['answer']})
    return res['answer']

# create_db("law.pdf")

def chatcusttomer(question):
    chat_history= get_chat_history()
    res = chat_llm2({"question": question, "chat_history": chat_history})
    # n=0
    # memory.clear()
    memory.save_context({"input": question}, {"output": res['answer']})
    return res['answer']

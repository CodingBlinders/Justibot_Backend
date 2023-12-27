from langchain import FAISS
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from llm import embeddings


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

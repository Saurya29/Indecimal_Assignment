import os

from langchain_community.document_loaders import TextLoader
from langchain_community.text_splitter import RecursiveCharacterTextSplitter

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS


# ---------------------------------------
# Load Markdown Documents
# ---------------------------------------
def load_documents(folder_path):
    """
    Reads all .md files from a folder and loads them as LangChain documents
    """
    documents = []

    for file in os.listdir(folder_path):
        if file.endswith(".md"):
            file_path = os.path.join(folder_path, file)
            loader = TextLoader(file_path, encoding="utf-8")
            documents.extend(loader.load())

    return documents


# ---------------------------------------
# Chunk Documents
# ---------------------------------------
def chunk_documents(documents):
    """
    Split documents into overlapping chunks
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)
    return chunks


# ---------------------------------------
# Create FAISS Vector Store
# ---------------------------------------
def create_vectorstore(chunks):
    """
    Create embeddings and store vectors in FAISS
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("faiss_index")

    return vectorstore


# ---------------------------------------
# Load Existing FAISS Vector Store
# ---------------------------------------
def load_vectorstore():
    """
    Load FAISS index from disk
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.load_local("faiss_index", embeddings)
    return vectorstore

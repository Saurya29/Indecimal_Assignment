import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def load_documents(folder_path="data"):
    documents = []

    for file in os.listdir(folder_path):
        if file.endswith(".md"):
            loader = TextLoader(
                os.path.join(folder_path, file),
                encoding="utf-8"
            )
            documents.extend(loader.load())

    return documents


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80
    )
    return splitter.split_documents(documents)


def create_vectorstore(chunks):
    if len(chunks) == 0:
        raise ValueError("No documents found inside data folder.")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("faiss_index")

    return vectorstore


def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

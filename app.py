import streamlit as st
from utils import load_documents, chunk_documents, create_vectorstore, load_vectorstore
from langchain.llms import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="Mini RAG Assistant",
    page_icon="🧱",
    layout="wide"
)

# ---------------------------
# Custom CSS
# ---------------------------
st.markdown("""
<style>

body {
    background-color: #0f172a;
}

.main-title {
    font-size: 2.4rem;
    font-weight: 700;
    color: #e5e7eb;
}

.subtitle {
    color: #94a3b8;
    margin-bottom: 30px;
}

.chat-user {
    background: #1e293b;
    padding: 14px;
    border-radius: 12px;
    margin-bottom: 10px;
}

.chat-bot {
    background: #020617;
    padding: 14px;
    border-radius: 12px;
    margin-bottom: 10px;
    border-left: 4px solid #6366f1;
}

.context-box {
    background: #020617;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid #1e293b;
    margin-bottom: 10px;
}

.sidebar-title {
    font-size: 1.3rem;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# Header
# ---------------------------
st.markdown("<div class='main-title'>🧱 Mini RAG Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Grounded Question Answering over Internal Documents</div>", unsafe_allow_html=True)

# ---------------------------
# Sidebar
# ---------------------------
st.sidebar.markdown("<div class='sidebar-title'>⚙ Controls</div>", unsafe_allow_html=True)

if st.sidebar.button("Build Knowledge Base"):
    with st.spinner("Processing documents..."):
        docs = load_documents("data")
        chunks = chunk_documents(docs)
        create_vectorstore(chunks)
    st.sidebar.success("Knowledge base built successfully")

# ---------------------------
# Load Vectorstore
# ---------------------------
try:
    vectorstore = load_vectorstore()
    ready = True
except:
    ready = False

llm = OpenAI(temperature=0)

# ---------------------------
# Chat Input
# ---------------------------
query = st.text_input("Ask a question about your documents")

if query and ready:

    st.markdown(f"<div class='chat-user'><b>You:</b> {query}</div>", unsafe_allow_html=True)

    docs = vectorstore.similarity_search(query, k=4)
    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
You are an AI assistant.

Answer ONLY using the context below.
If answer not found, say:
"I don't know based on the provided documents."

Context:
{context}

Question:
{query}

Answer:
"""

    answer = llm.invoke(prompt)

    st.markdown(f"<div class='chat-bot'><b>Assistant:</b> {answer}</div>", unsafe_allow_html=True)

    # Retrieved context
    st.subheader("📚 Retrieved Context")

    for i, d in enumerate(docs):
        st.markdown(f"<div class='context-box'><b>Chunk {i+1}</b><br>{d.page_content}</div>", unsafe_allow_html=True)

elif query and not ready:
    st.warning("Please build knowledge base first")

# ---------------------------
# Footer
# ---------------------------
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit, FAISS & Sentence Transformers")

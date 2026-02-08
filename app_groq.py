from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
import streamlit as st

from utils import load_documents, chunk_documents, create_vectorstore, load_vectorstore
from langchain_groq import ChatGroq


# ----------------------------------
# Load ENV
# ----------------------------------
load_dotenv()

# ----------------------------------
# Page Config
# ----------------------------------
st.set_page_config(
    page_title="Construction Marketplace Mini-RAG",
    layout="wide"
)

# ----------------------------------
# Styling
# ----------------------------------
st.markdown("""
<style>

body { background-color:#0b0f19; }

.title {
    font-size:2.6rem;
    font-weight:800;
    color:#f8fafc;
}

.subtitle {
    color:#94a3b8;
    margin-bottom:25px;
}

.card {
    background:linear-gradient(145deg,#020617,#0f172a);
    padding:20px;
    border-radius:14px;
    margin-bottom:14px;
    animation:fade 0.4s ease-in-out;
    font-size:1.05rem;
    line-height:1.7;
}

.user { border-left:5px solid #22c55e; }

.bot {
    border-left:5px solid #6366f1;
    font-size:1.15rem;
}

.chunk {
    background:#020617;
    padding:14px;
    border-radius:10px;
    border:1px solid #1e293b;
    margin-bottom:10px;
}

@keyframes fade {
    from {opacity:0; transform:translateY(10px);}
    to {opacity:1; transform:translateY(0);}
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------
# Header with Logo
# ----------------------------------
col1, col2 = st.columns([1,8])

with col1:
    st.image("logo.png", width=200)

with col2:
    st.markdown("<div class='title'>Construction Marketplace Mini-RAG</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Groq Cloud LLM + FAISS + Grounded QA</div>", unsafe_allow_html=True)

# ----------------------------------
# Session State
# ----------------------------------
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

# ----------------------------------
# Auto Build / Load Vector Store
# ----------------------------------
if st.session_state.vectorstore is None:
    try:
        st.session_state.vectorstore = load_vectorstore()
    except:
        with st.spinner("Building knowledge base from documents..."):
            docs = load_documents("data")
            chunks = chunk_documents(docs)
            create_vectorstore(chunks)
            st.session_state.vectorstore = load_vectorstore()

# ----------------------------------
# Groq LLM
# ----------------------------------
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant",
    temperature=0
)

# ----------------------------------
# User Input
# ----------------------------------
query = st.text_input("Ask about policies, pricing, quality, delays, warranties...")

if query and st.session_state.vectorstore is not None:

    st.markdown(
        f"<div class='card user'><b>You:</b> {query}</div>",
        unsafe_allow_html=True
    )

    # ----------------------------------
    # Retrieval
    # ----------------------------------
    retrieved = st.session_state.vectorstore.similarity_search_with_score(query, k=3)

    context = ""
    for i, (doc, score) in enumerate(retrieved):
        context += f"\n\n[Chunk {i+1}]\n{doc.page_content[:1200]}"

    # ----------------------------------
    # STRICT RAG PROMPT
    # ----------------------------------
    prompt = f"""
You are a retrieval-augmented QA system.

Rules:
1. Use ONLY the context below.
2. Do NOT use outside knowledge.
3. If answer not present, reply exactly:
NOT FOUND IN DOCUMENTS

CONTEXT:
{context}

QUESTION:
{query}

Return format:

ANSWER:
- bullet point
- bullet point
- bullet point

SOURCE_CHUNKS:
- Chunk numbers used
"""

    # Grounding indicator
    st.info("🛡️ Generating answer strictly from retrieved document context...")

    response = llm.invoke(prompt).content

    if "NOT FOUND IN DOCUMENTS" in response:
        st.error("Answer not present in provided documents.")
        st.stop()

    st.markdown(
        f"<div class='card bot'><b>Assistant:</b><br>{response}</div>",
        unsafe_allow_html=True
    )

    # ----------------------------------
    # Transparency
    # ----------------------------------
    st.subheader("📚 Retrieved Context")

    for i, (doc, score) in enumerate(retrieved):
        st.markdown(
            f"<div class='chunk'><b>Chunk {i+1} | Similarity: {round(score,4)}</b><br>{doc.page_content}</div>",
            unsafe_allow_html=True
        )

# ----------------------------------
# Footer
# ----------------------------------
st.markdown("---")
st.markdown("Mini-RAG | FAISS + Sentence-Transformers + Groq LLM")

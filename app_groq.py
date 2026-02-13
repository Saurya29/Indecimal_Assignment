from dotenv import load_dotenv
import os
import streamlit as st

from utils import load_documents, chunk_documents, create_vectorstore, load_vectorstore
from langchain_groq import ChatGroq

# ---------------------------
# Load Env
# ---------------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="Construction Marketplace Mini-RAG",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------
# Global Dark Theme + Bigger Fonts
# ---------------------------
st.markdown("""
<style>

/* App Background */
html, body, [data-testid="stApp"] {
    background-color:#0b0f19;
    color:#e5e7eb;
    font-size:18px;
}

/* Headings */
h1 {font-size:3rem !important;}
h2 {font-size:2.2rem !important;}
h3 {font-size:1.7rem !important;}
p, li, span, label, input {
    font-size:1.05rem !important;
}

/* Input */
input {
    background:#020617 !important;
    color:white !important;
    border:1px solid #334155 !important;
    border-radius:10px !important;
    padding:14px !important;
}

/* Buttons */
button {
    background:#4f46e5 !important;
    color:white !important;
    border-radius:10px !important;
    padding:10px 18px !important;
    font-size:1rem !important;
}

/* Card */
.card {
    background:linear-gradient(145deg,#020617,#0f172a);
    padding:22px;
    border-radius:16px;
    margin-bottom:18px;
    line-height:1.8;
    box-shadow:0 0 12px rgba(99,102,241,0.15);
}

/* User vs Bot */
.user {border-left:6px solid #22c55e;}
.bot  {border-left:6px solid #6366f1;}

/* Chunk */
.chunk {
    background:#020617;
    padding:16px;
    border-radius:12px;
    border:1px solid #1e293b;
    margin-bottom:12px;
}

/* Pills */
.pill {
    display:inline-block;
    padding:8px 14px;
    background:#1e293b;
    border-radius:999px;
    margin:6px 6px 0 0;
    font-size:0.95rem;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# Header
# ---------------------------
st.markdown("""
<h1>🏗 Construction Marketplace Mini-RAG</h1>
<p style="color:#94a3b8;">
Ask questions about pricing, quality, delays, warranties, packages, materials, and maintenance —  
answers come strictly from internal construction documents.
</p>
""", unsafe_allow_html=True)

# ---------------------------
# Suggested Questions
# ---------------------------
with st.expander("💡 What can I ask?", expanded=True):
    st.markdown("""
<div class="pill">What is the escrow-based payment system?</div>
<div class="pill">How does Indecimal handle construction delays?</div>
<div class="pill">What are the package prices per sqft?</div>
<div class="pill">What materials are used in Premier package?</div>
<div class="pill">How many quality checkpoints exist?</div>
<div class="pill">What does zero-cost maintenance cover?</div>
<div class="pill">Do you provide real-time tracking?</div>
<div class="pill">What warranties are offered?</div>
<div class="pill">Explain stage-based contractor payments</div>
<div class="pill">What is included in kitchen wallet?</div>
<div class="pill">Bathroom fittings allowance?</div>
<div class="pill">What brands of cement are used?</div>
""", unsafe_allow_html=True)

# ---------------------------
# Session State
# ---------------------------
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

# ---------------------------
# Load Vector DB
# ---------------------------
if st.session_state.vectorstore is None:
    try:
        st.session_state.vectorstore = load_vectorstore()
    except:
        with st.spinner("Building knowledge base..."):
            docs = load_documents("data")
            chunks = chunk_documents(docs)
            create_vectorstore(chunks)
            st.session_state.vectorstore = load_vectorstore()

# ---------------------------
# LLM
# ---------------------------
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant",
    temperature=0
)

# ---------------------------
# Query Box
# ---------------------------
query = st.text_input("🔍 Ask your question")

# ---------------------------
# RAG Pipeline
# ---------------------------
if query and st.session_state.vectorstore:

    st.markdown(
        f"<div class='card user'><b>You:</b><br>{query}</div>",
        unsafe_allow_html=True
    )

    retrieved = st.session_state.vectorstore.similarity_search_with_score(query, k=3)

    context = ""
    for i, (doc, score) in enumerate(retrieved):
        context += f"\n\n[Chunk {i+1}]\n{doc.page_content[:1200]}"

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

SOURCE_CHUNKS:
- Chunk numbers used
"""

    with st.spinner("Generating answer..."):
        response = llm.invoke(prompt).content

    if "NOT FOUND IN DOCUMENTS" in response:
        st.error("Answer not present in documents.")
        st.stop()

    st.markdown(
        f"<div class='card bot'><b>Assistant:</b><br>{response}</div>",
        unsafe_allow_html=True
    )

    # ---------------------------
    # Retrieved Context
    # ---------------------------
    st.subheader("📚 Retrieved Context")

    for i, (doc, score) in enumerate(retrieved):
        st.markdown(
            f"<div class='chunk'><b>Chunk {i+1} | Similarity: {round(score,4)}</b><br>{doc.page_content}</div>",
            unsafe_allow_html=True
        )

# ---------------------------
# Footer
# ---------------------------
st.markdown("---")
st.markdown(
"Mini-RAG System | FAISS • Sentence-Transformers • Groq LLM",
unsafe_allow_html=True
)

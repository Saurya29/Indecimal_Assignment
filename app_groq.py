from dotenv import load_dotenv
import os
import streamlit as st
from utils import load_documents, chunk_documents, create_vectorstore, load_vectorstore
from langchain_groq import ChatGroq

# -------------------------
# LOAD ENV
# -------------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Construction Intelligence AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------
# MODERN CLEAN CSS
# -------------------------
st.markdown("""
<style>

/* ================= BASE ================= */
html, body, [data-testid="stApp"]{
    background:#020617;
    color:#e5e7eb;
    font-family: 'Segoe UI', sans-serif;
}

/* ================= HERO ================= */
.logo-hero{
    position:relative;
    padding:140px 40px 80px 40px;
    border-radius:30px;
    margin-bottom:50px;
    text-align:center;

    background:
    radial-gradient(circle at top left, #4f46e5 0%, transparent 45%),
    radial-gradient(circle at bottom right, #22c55e 0%, transparent 45%),
    linear-gradient(145deg,#020617,#0b1225);

    box-shadow:
    0 0 90px rgba(99,102,241,0.55),
    inset 0 0 40px rgba(34,197,94,0.18);

    overflow:hidden;
}

/* BIG LOGO */
.logo-hero::before{
    content:"";
    position:absolute;
    inset:0;
    background:url("logo.png") no-repeat center 40px;
    background-size:120px;
    opacity:0.12;
    filter:drop-shadow(0 0 30px rgba(99,102,241,0.6));
}

/* TEXT CONTAINER */
.logo-hero-content{
    position:relative;
    z-index:2;
}

/* TITLE */
.logo-hero h1{
    margin-top:320px;
    font-size:3.4rem !important;
    font-weight:900;
    background:linear-gradient(90deg,#a5b4fc,#22c55e);
    -webkit-background-clip:text;
    color:transparent;
}

/* SUBTITLE */
.logo-hero p{
    font-size:1.2rem !important;
    margin-top:15px;
    color:#c7d2fe;
    max-width:900px;
    margin-left:auto;
    margin-right:auto;
}

/* ================= INPUT ================= */
input{
    background:#020617 !important;
    color:white !important;
    font-size:1.15rem !important;
    padding:18px !important;
    border-radius:14px !important;
    border:1px solid #6366f1 !important;
}

/* ================= BUTTON ================= */
button{
    background:#4f46e5 !important;
    color:white !important;
    font-size:1rem !important;
    border-radius:12px !important;
    padding:10px 20px !important;
}

/* ================= CARDS ================= */
.card{
    background:rgba(2,6,23,0.75);
    backdrop-filter:blur(12px);
    padding:28px;
    border-radius:20px;
    margin-bottom:22px;
    box-shadow:0 0 25px rgba(99,102,241,0.25);
}

.user{
    border-left:6px solid #22c55e;
}

.bot{
    border-left:6px solid #6366f1;
}

/* ================= CHUNKS ================= */
.chunk{
    background:#020617;
    padding:20px;
    border-radius:16px;
    border:1px solid #1e293b;
    margin-bottom:14px;
    font-size:1rem;
    line-height:1.6;
}

/* ================= SUGGESTION PILLS ================= */
.pill{
    display:inline-block;
    padding:8px 16px;
    border-radius:999px;
    background:#1e293b;
    margin:6px;
    font-size:0.95rem;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# HERO SECTION
# -------------------------
st.markdown("""
<div class="logo-hero">
  <div class="logo-hero-content">
    <h1>Construction Intelligence AI</h1>
    <p>
      AI-powered assistant for construction pricing, quality systems,
      materials, warranties, delays and maintenance using verified internal documents.
    </p>
  </div>
</div>
""", unsafe_allow_html=True)

# -------------------------
# SUGGESTED QUESTIONS
# -------------------------
with st.expander("✨ Suggested Questions", expanded=True):
    st.markdown("""
    <div class="pill">What are the package prices per sqft?</div>
    <div class="pill">Explain escrow-based payment system</div>
    <div class="pill">How many quality checkpoints exist?</div>
    <div class="pill">How are construction delays handled?</div>
    <div class="pill">What materials are used in Premier package?</div>
    <div class="pill">What does zero cost maintenance include?</div>
    <div class="pill">Do you provide real-time tracking?</div>
    <div class="pill">What warranty is provided?</div>
    """, unsafe_allow_html=True)

# -------------------------
# VECTORSTORE
# -------------------------
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if st.session_state.vectorstore is None:
    try:
        st.session_state.vectorstore = load_vectorstore()
    except:
        with st.spinner("Building knowledge base..."):
            docs = load_documents("data")
            chunks = chunk_documents(docs)
            create_vectorstore(chunks)
            st.session_state.vectorstore = load_vectorstore()

# -------------------------
# LLM
# -------------------------
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant",
    temperature=0
)

# -------------------------
# QUERY INPUT
# -------------------------
query = st.text_input("🔍 Ask a question about construction policies, pricing, quality, materials...")

# -------------------------
# RAG PIPELINE
# -------------------------
if query and st.session_state.vectorstore:

    st.markdown(f"<div class='card user'><b>You</b><br>{query}</div>", unsafe_allow_html=True)

    retrieved = st.session_state.vectorstore.similarity_search_with_score(query, k=3)

    context = ""
    for i, (doc, score) in enumerate(retrieved):
        context += f"\n\n[Chunk {i+1}]\n{doc.page_content[:1200]}"

    prompt = f"""
You are a strict retrieval-augmented QA system.

Rules:
1. Use ONLY the provided context.
2. If the answer is missing, reply exactly:
NOT FOUND IN DOCUMENTS

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
- bullet point
- bullet point

SOURCE_CHUNKS:
- chunk numbers used
"""

    with st.spinner("Generating answer..."):
        response = llm.invoke(prompt).content

    if "NOT FOUND" in response:
        st.error("Answer not found in documents.")
        st.stop()

    st.markdown(f"<div class='card bot'><b>Assistant</b><br>{response}</div>", unsafe_allow_html=True)

    st.subheader("📚 Retrieved Context")

    for i, (doc, score) in enumerate(retrieved):
        st.markdown(
            f"<div class='chunk'><b>Chunk {i+1}</b><br>{doc.page_content}</div>",
            unsafe_allow_html=True
        )

st.markdown("---")
st.markdown("Mini-RAG | FAISS • Sentence Transformers • Groq LLM")

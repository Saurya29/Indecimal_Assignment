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
    font-size:20px;   /* GLOBAL SCALE UP */
}

/* ================= HERO ================= */
.logo-hero{
    position:relative;
    padding:40px 20px 25px 20px;   /* REDUCED */
    border-radius:26px;
    margin-bottom:40px;
    text-align:center;

    background:
    radial-gradient(circle at top left, #4f46e5 0%, transparent 45%),
    radial-gradient(circle at bottom right, #22c55e 0%, transparent 45%),
    linear-gradient(145deg,#020617,#0b1225);

    box-shadow:
    0 0 60px rgba(99,102,241,0.45),
    inset 0 0 30px rgba(34,197,94,0.15);
}

/* BIG LOGO */
.logo-hero::before{
    content:"";
    position:absolute;
    inset:0;
    background:url("logo.png") no-repeat center 25px;
    background-size:100px;  /* SMALLER */
    opacity:0.14;
}

/* TITLE */
.logo-hero h1{
    margin-top:190px;     /* MOVED UP */
    font-size:3.1rem !important;
    font-weight:900;
    background:linear-gradient(90deg,#a5b4fc,#22c55e);
    -webkit-background-clip:text;
    color:transparent;
}

/* SUBTITLE */
.logo-hero p{
    font-size:1.35rem !important;
    margin-top:12px;
    color:#c7d2fe;
}

/* ================= INPUT ================= */
input{
    background:#020617 !important;
    color:white !important;
    font-size:1.25rem !important;
    padding:18px !important;
    border-radius:14px !important;
    border:1px solid #6366f1 !important;
}

/* ================= CARDS ================= */
.card{
    background:rgba(2,6,23,0.75);
    padding:28px;
    border-radius:20px;
    margin-bottom:22px;
    box-shadow:0 0 20px rgba(99,102,241,0.25);
}

.card b{
    font-size:1.3rem;
}

/* ================= CHUNKS ================= */
.chunk{
    background:#020617;
    padding:22px;
    border-radius:16px;
    border:1px solid #1e293b;
    margin-bottom:14px;
    font-size:1.1rem;
    line-height:1.7;
}

/* ================= PILLS ================= */
.pill{
    display:inline-block;
    padding:10px 18px;
    border-radius:999px;
    background:#1e293b;
    margin:6px;
    font-size:1.05rem;
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

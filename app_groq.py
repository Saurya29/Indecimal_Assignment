from dotenv import load_dotenv
import os
import streamlit as st
from utils import load_documents, chunk_documents, create_vectorstore, load_vectorstore
from langchain_groq import ChatGroq

# -----------------------
# Load ENV
# -----------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# -----------------------
# Page Config
# -----------------------
st.set_page_config(
    page_title="Construction Intelligence AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------
# STABLE MODERN CSS + NEON
# -----------------------
st.markdown("""
<style>

/* ---------------- BASE ---------------- */
html, body, [data-testid="stApp"]{
background:
radial-gradient(circle at top left,#1e1b4b 0%,transparent 40%),
radial-gradient(circle at bottom right,#052e16 0%,transparent 40%),
#020617;
color:#e5e7eb;
font-family:'Segoe UI',sans-serif;
}

/* Watermark logo */
[data-testid="stApp"]::before{
content:"";
position:fixed;
top:50%;
left:50%;
transform:translate(-50%,-50%);
width:700px;
height:700px;
background:url("logo.png") no-repeat center;
background-size:contain;
opacity:0.04;
z-index:-1;
}

/* ---------------- TYPOGRAPHY ---------------- */
h1{font-size:3rem !important;}
h2{font-size:2.1rem !important;}
h3{font-size:1.6rem !important;}
p, span, label, li, div{
font-size:1.08rem !important;
line-height:1.75;
}

/* ---------------- INPUT ---------------- */
input{
background:#020617!important;
color:white!important;
font-size:1.15rem!important;
padding:16px!important;
border-radius:12px!important;
border:1px solid #6366f1!important;
box-shadow:0 0 12px rgba(99,102,241,.5);
}

/* ---------------- BUTTON ---------------- */
button{
background:#4f46e5!important;
color:white!important;
font-size:1rem!important;
border-radius:12px!important;
padding:10px 20px!important;
box-shadow:0 0 12px rgba(99,102,241,.6);
}

/* ---------------- CARDS ---------------- */
.card{
background:rgba(2,6,23,0.78);
backdrop-filter:blur(14px);
padding:24px;
border-radius:18px;
margin-bottom:18px;
box-shadow:0 0 25px rgba(99,102,241,.35);
animation:fadeUp .4s ease;
}

.user{border-left:6px solid #22c55e;}
.bot{border-left:6px solid #6366f1;}

.card:hover{
transform:scale(1.01);
transition:.25s;
}

/* ---------------- PILLS ---------------- */
.pill-btn button{
background:#1e293b!important;
border-radius:999px!important;
padding:8px 16px!important;
font-size:.95rem!important;
box-shadow:0 0 10px rgba(79,70,229,.6);
}

/* ---------------- CHUNKS ---------------- */
.chunk{
background:#020617;
padding:18px;
border-radius:14px;
border:1px solid #1e293b;
margin-bottom:12px;
}

/* ---------------- ANIMATION ---------------- */
@keyframes fadeUp{
from{opacity:0;transform:translateY(20px);}
to{opacity:1;transform:translateY(0);}
}

</style>
""", unsafe_allow_html=True)

# -----------------------
# HEADER
# -----------------------
col1,col2=st.columns([1,6])

with col1:
    st.image("logo.png", width=120)

with col2:
    st.markdown("""
    <h1>Construction Intelligence AI</h1>
    <p>Ask verified questions about pricing, quality, delays, warranties and materials.</p>
    """, unsafe_allow_html=True)

# -----------------------
# CLICKABLE PILLS
# -----------------------
suggested = [
"What are the package prices per sqft?",
"Explain escrow based payment system",
"How many quality checkpoints exist?",
"How are construction delays handled?",
"What materials are used in Premier package?",
"What does zero cost maintenance include?",
"Do you provide real time tracking?",
"What warranty is provided?"
]

with st.expander("✨ Suggested Questions", expanded=True):
    cols = st.columns(4)
    for i, text in enumerate(suggested):
        with cols[i % 4]:
            if st.button(text, key=f"sug_{i}"):
                st.session_state["query_box"] = text

# -----------------------
# VECTORSTORE
# -----------------------
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore=None

if st.session_state.vectorstore is None:
    try:
        st.session_state.vectorstore=load_vectorstore()
    except:
        with st.spinner("Indexing documents..."):
            docs=load_documents("data")
            chunks=chunk_documents(docs)
            create_vectorstore(chunks)
            st.session_state.vectorstore=load_vectorstore()

# -----------------------
# LLM
# -----------------------
llm=ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant",
    temperature=0
)

# -----------------------
# INPUT (AUTOFILL ENABLED)
# -----------------------
query=st.text_input(
    "🔍 Ask your question",
    key="query_box"
)

# -----------------------
# RAG PIPELINE
# -----------------------
if query and st.session_state.vectorstore:

    st.markdown(
        f"<div class='card user'><b>You</b><br>{query}</div>",
        unsafe_allow_html=True
    )

    retrieved=st.session_state.vectorstore.similarity_search_with_score(query,k=3)

    context=""
    for i,(doc,score) in enumerate(retrieved):
        context+=f"\n\n[Chunk {i+1}]\n{doc.page_content[:1200]}"

    prompt=f"""
You are a retrieval-augmented QA system.

Rules:
1. Use ONLY context
2. If missing say NOT FOUND IN DOCUMENTS

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
- bullet
- bullet

SOURCE_CHUNKS:
- numbers
"""

    with st.spinner("Generating answer..."):
        response=llm.invoke(prompt).content

    if "NOT FOUND" in response:
        st.error("Answer not found in documents.")
        st.stop()

    st.markdown(
        f"<div class='card bot'><b>Assistant</b><br>{response}</div>",
        unsafe_allow_html=True
    )

    st.subheader("📚 Retrieved Context")

    for i,(doc,score) in enumerate(retrieved):
        st.markdown(
            f"<div class='chunk'><b>Chunk {i+1}</b><br>{doc.page_content}</div>",
            unsafe_allow_html=True
        )

st.markdown("---")
st.markdown("Mini-RAG | FAISS • Sentence Transformers • Groq")

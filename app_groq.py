from dotenv import load_dotenv
import os
import streamlit as st
from utils import load_documents, chunk_documents, create_vectorstore, load_vectorstore
from langchain_groq import ChatGroq
<<<<<<< HEAD
import base64

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg_image = get_base64_image("construction_bg.jpg")
logo_image = get_base64_image("logo.png")

st.set_page_config(
    page_title="Construction Marketplace AI",
=======

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
>>>>>>> 9684c1f89e0f2e54af5bf8a0f527b56b057b00fe
    layout="wide",
    initial_sidebar_state="collapsed"
)

<<<<<<< HEAD
st.markdown(f"""
<style>

html, body, [data-testid="stApp"] {{
    background:
    linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)),
    url("data:image/jpg;base64,{bg_image}") no-repeat center fixed;
    background-size:cover;
    color:white;
    font-family:Segoe UI,sans-serif;
}}

.block-container {{
    padding-top:1.3rem;
}}

.hero-header {{
    display:flex;
    align-items:center;
    justify-content:center;
    gap:25px;
    margin-top:30px;
    margin-bottom:20px;
}}

.hero-logo {{
    width:155px;
    filter:drop-shadow(0 0 12px #f97316);
    animation:glow 2s infinite alternate;
}}

@keyframes glow {{
    from {{ filter:drop-shadow(0 0 6px #f97316); }}
    to {{ filter:drop-shadow(0 0 20px #f97316); }}
}}

.hero-title {{
    font-size:3.7rem;
    font-weight:900;
    color:#f97316;
}}

.hero-subtitle {{
    font-size:1.3rem;
    text-align:center;
    max-width:900px;
    margin:20px auto 110px auto;
    color:#f1f5f9;
}}

.custom-label {{
    font-size:1.6rem;
    font-weight:700;
    color:#f97316;
    margin-bottom:6px;
}}

input {{
    background:#000000b0!important;
    color:white!important;
    font-size:1.2rem!important;
    padding:16px!important;
    border-radius:10px!important;
    border:1px solid #f97316!important;
}}

button {{
    background:#f97316!important;
    color:white!important;
    font-size:1.05rem!important;
    border-radius:10px!important;
}}

.card {{
    background:#000000b5;
    padding:20px;
    border-radius:10px;
    border-left:5px solid #f97316;
    margin-bottom:15px;
}}

.chunk {{
    background:#00000090;
    padding:16px;
    border-radius:10px;
    margin-bottom:10px;
}}
=======
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

.main-title{
    font-size:4.2rem !important;   /* Increase here */
    font-weight:800;
    letter-spacing:1px;
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
>>>>>>> 9684c1f89e0f2e54af5bf8a0f527b56b057b00fe

</style>
""", unsafe_allow_html=True)

<<<<<<< HEAD
st.markdown(f"""
<div class="hero-header">
    <img src="data:image/png;base64,{logo_image}" class="hero-logo">
    <div class="hero-title">Construction Marketplace AI</div>
</div>

<div class="hero-subtitle">
AI-powered assistant for pricing, quality, materials, warranties, delays and maintenance using verified internal documents.
</div>
""", unsafe_allow_html=True)

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

with st.expander("Suggested Questions"):
    cols = st.columns(4)
    for i, q in enumerate(suggested):
        with cols[i % 4]:
            if st.button(q, key=f"s{i}"):
                st.session_state["query"] = q

=======
# -----------------------
# HEADER
# -----------------------
col1,col2=st.columns([1,6])

with col1:
    st.image("logo.png", width=120)

with col2:
    st.markdown("""
    <h1 class="main-title">Construction Intelligence AI</h1>
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
>>>>>>> 9684c1f89e0f2e54af5bf8a0f527b56b057b00fe
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore=None

if st.session_state.vectorstore is None:
    try:
        st.session_state.vectorstore=load_vectorstore()
    except:
        with st.spinner("Indexing documents..."):
<<<<<<< HEAD
            docs = load_documents("data")
            chunks = chunk_documents(docs)
=======
            docs=load_documents("data")
            chunks=chunk_documents(docs)
>>>>>>> 9684c1f89e0f2e54af5bf8a0f527b56b057b00fe
            create_vectorstore(chunks)
            st.session_state.vectorstore=load_vectorstore()

<<<<<<< HEAD
llm = ChatGroq(
=======
# -----------------------
# LLM
# -----------------------
llm=ChatGroq(
>>>>>>> 9684c1f89e0f2e54af5bf8a0f527b56b057b00fe
    api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant",
    temperature=0
)

<<<<<<< HEAD
st.markdown("<div class='custom-label'>Ask your question</div>", unsafe_allow_html=True)
query = st.text_input("Ask", key="query", label_visibility="collapsed")

if query and st.session_state.vectorstore:

    st.markdown(f"<div class='card'><b>You:</b><br>{query}</div>", unsafe_allow_html=True)

    results = st.session_state.vectorstore.similarity_search_with_score(query, k=3)

    results = [(doc, score) for doc, score in results if score < 1.2]

    if len(results) == 0:
        st.error("Answer not found in documents.")
        st.stop()

    context = ""
    for i, (doc, score) in enumerate(results):
        context += f"\n\n[Chunk {i+1}]\n{doc.page_content[:1200]}"

    prompt = f"""
You are a strict retrieval-based assistant.

Rules:
1. Use ONLY the provided context.
2. If answer is not present, reply exactly: NOT FOUND.
3. Do not guess or use outside knowledge.
=======
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
>>>>>>> 9684c1f89e0f2e54af5bf8a0f527b56b057b00fe

CONTEXT:
{context}

QUESTION:
{query}

<<<<<<< HEAD
If answer exists:
- bullet points
- mention chunk numbers

If missing:
NOT FOUND
"""

    with st.spinner("Generating answer..."):
        response = llm.invoke(prompt).content.strip()

    if response.upper() == "NOT FOUND":
        st.error("Answer not found in documents.")
        st.stop()

    st.markdown(f"<div class='card'><b>Assistant:</b><br>{response}</div>", unsafe_allow_html=True)

    st.subheader("Retrieved Context")

    for i, (doc, score) in enumerate(results):
=======
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
>>>>>>> 9684c1f89e0f2e54af5bf8a0f527b56b057b00fe
        st.markdown(
            f"<div class='chunk'><b>Chunk {i+1}</b><br>{doc.page_content}</div>",
            unsafe_allow_html=True
        )

st.markdown("---")
<<<<<<< HEAD
st.markdown("Powered by FAISS • Sentence Transformers • Groq")
=======
st.markdown("Mini-RAG | FAISS • Sentence Transformers • Groq")
>>>>>>> 9684c1f89e0f2e54af5bf8a0f527b56b057b00fe

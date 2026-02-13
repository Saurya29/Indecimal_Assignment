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
    layout="wide"
)

# -----------------------
# Ultra Modern CSS
# -----------------------
st.markdown("""
<style>

/* ===== GLOBAL ===== */
html, body, [data-testid="stApp"]{
background:#020617;
color:#e5e7eb;
font-family: 'Segoe UI', sans-serif;
}

/* ===== 3D HERO BACKGROUND ===== */
.hero {
background:
radial-gradient(circle at top left, #4f46e5 0%, transparent 40%),
radial-gradient(circle at bottom right, #22c55e 0%, transparent 40%),
url("https://images.unsplash.com/photo-1503387762-592deb58ef4e");
background-size:cover;
padding:80px 60px;
border-radius:30px;
margin-bottom:40px;
box-shadow:0 0 80px rgba(99,102,241,0.6);
animation:fadeUp 1s ease;
}

/* ===== TITLES ===== */
.hero h1{
font-size:4rem;
font-weight:900;
background:linear-gradient(90deg,#a5b4fc,#22c55e);
-webkit-background-clip:text;
color:transparent;
}

.hero p{
font-size:1.3rem;
color:#c7d2fe;
max-width:800px;
}

/* ===== INPUT ===== */
input{
background:#020617!important;
border-radius:14px!important;
padding:18px!important;
font-size:1.1rem!important;
border:1px solid #4f46e5!important;
}

/* ===== CARDS ===== */
.card{
background:rgba(2,6,23,0.7);
backdrop-filter:blur(18px);
padding:26px;
border-radius:20px;
margin-bottom:18px;
animation:fadeUp .6s ease;
box-shadow:0 0 20px rgba(99,102,241,0.25);
}

.user{border-left:6px solid #22c55e;}
.bot{border-left:6px solid #6366f1;}

.card:hover{
transform:scale(1.02);
transition:0.3s;
}

/* ===== PILLS ===== */
.pill{
display:inline-block;
padding:10px 18px;
border-radius:999px;
background:#1e293b;
margin:6px;
box-shadow:0 0 12px rgba(79,70,229,0.4);
}

/* ===== CHUNKS ===== */
.chunk{
background:#020617;
border-radius:16px;
padding:20px;
margin-bottom:14px;
border:1px solid #1e293b;
}

/* ===== ANIMATIONS ===== */
@keyframes fadeUp{
from{opacity:0;transform:translateY(30px);}
to{opacity:1;transform:translateY(0);}
}

</style>
""", unsafe_allow_html=True)

# -----------------------
# HERO SECTION
# -----------------------
st.markdown("""
<div class="hero">
<h1>🏗 Construction Intelligence AI</h1>
<p>
AI-powered assistant for construction pricing, quality systems,
materials, warranties, delays, and maintenance using verified internal documents.
</p>
</div>
""", unsafe_allow_html=True)

# -----------------------
# SUGGESTED PROMPTS
# -----------------------
with st.expander("✨ Suggested Questions", expanded=True):
    st.markdown("""
<div class="pill">What are the package prices per sqft?</div>
<div class="pill">Explain escrow based payments</div>
<div class="pill">How does Indecimal ensure quality?</div>
<div class="pill">What materials are used in Premier package?</div>
<div class="pill">What does zero cost maintenance cover?</div>
<div class="pill">How are delays handled?</div>
<div class="pill">Do you provide real time tracking?</div>
<div class="pill">What warranty is offered?</div>
""", unsafe_allow_html=True)

# -----------------------
# VECTOR DB
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
# INPUT
# -----------------------
query=st.text_input("Ask anything about construction policies, pricing or quality")

# -----------------------
# RAG FLOW
# -----------------------
if query and st.session_state.vectorstore:

    st.markdown(f"<div class='card user'><b>You</b><br>{query}</div>",unsafe_allow_html=True)

    retrieved=st.session_state.vectorstore.similarity_search_with_score(query,k=3)

    context=""
    for i,(doc,score) in enumerate(retrieved):
        context+=f"\n\n[Chunk {i+1}]\n{doc.page_content[:1200]}"

    prompt=f"""
You are a strict retrieval QA system.

Use only CONTEXT.
If answer missing say:
NOT FOUND IN DOCUMENTS.

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

    with st.spinner("Thinking..."):
        response=llm.invoke(prompt).content

    if "NOT FOUND" in response:
        st.error("Not found in documents.")
        st.stop()

    st.markdown(f"<div class='card bot'><b>Assistant</b><br>{response}</div>",unsafe_allow_html=True)

    st.subheader("📚 Source Context")

    for i,(doc,score) in enumerate(retrieved):
        st.markdown(
        f"<div class='chunk'><b>Chunk {i+1}</b><br>{doc.page_content}</div>",
        unsafe_allow_html=True
        )

st.markdown("---")
st.markdown("⚡ Powered by FAISS • Sentence Transformers • Groq LLM")


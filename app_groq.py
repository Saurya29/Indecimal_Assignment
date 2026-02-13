from dotenv import load_dotenv
import os
import streamlit as st
from utils import load_documents, chunk_documents, create_vectorstore, load_vectorstore
from langchain_groq import ChatGroq
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
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
    margin:20px auto 70px auto;
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

</style>
""", unsafe_allow_html=True)

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

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if st.session_state.vectorstore is None:
    try:
        st.session_state.vectorstore = load_vectorstore()
    except:
        with st.spinner("Indexing documents..."):
            docs = load_documents("data")
            chunks = chunk_documents(docs)
            create_vectorstore(chunks)
            st.session_state.vectorstore = load_vectorstore()

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant",
    temperature=0
)

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

CONTEXT:
{context}

QUESTION:
{query}

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
        st.markdown(
            f"<div class='chunk'><b>Chunk {i+1}</b><br>{doc.page_content}</div>",
            unsafe_allow_html=True
        )

st.markdown("---")
st.markdown("Powered by FAISS • Sentence Transformers • Groq")

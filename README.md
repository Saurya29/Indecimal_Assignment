#  Indecimal Construction Marketplace Mini-RAG
 Created By Saurya Raj , BTECH/10065/22

This project implements a **Retrieval-Augmented Generation (RAG)** based AI assistant for a construction marketplace.  
The assistant answers user queries strictly using internal documents such as policies, FAQs, and specifications instead of relying on general model knowledge.

The system demonstrates document chunking, embedding generation, semantic retrieval, and grounded answer generation using a Large Language Model (LLM).

---

## Objective

Build a simple RAG pipeline that:

- Retrieves relevant information from internal documents  
- Generates answers grounded only in retrieved content  
- Clearly displays retrieved context and final answer  

---

##  Features

- Chunking and embedding of internal documents  
- Local FAISS vector index  
- Semantic search for top-k relevant chunks  
- Local open-source LLM via Ollama  
- Grounded answer generation  
- Transparent display of retrieved chunks  
- Modern Streamlit frontend  

---

##  System Architecture
 User Query --> FAISS Vector Search --> Top-k Relevant Chunks --> Prompt + Context --> LLM = Ollama(Local Inference)|Grok (Cloud via Streamlit) --> Grounded Answer + Source Chunks

## Install Ollama

1. Download from:

    https://ollama.com/download

2. Pull model:

    ollama pull llama3.2:3b

3. Run Application
    streamlit run app.py

## 🔁 LLM Backend Comparison (Local vs Cloud)

| Aspect | Ollama (Local LLM) | Groq (Cloud LLM) |
|------|------------------|-----------------|
| Model Used | llama3.2:3b | llama-3.1-8b-instant |
| Cost | Free | Free tier |
| Latency | ~3–6 seconds | ~1–2 seconds |
| Answer Quality | Good | Very Good |
| Groundedness to Context | Strong | Strong |
| Hallucinations | None observed | None observed |
| Offline Usage | Yes | No |
| Setup Complexity | Medium | Easy |
| Internet Required | No | Yes |
| Best Use Case | Fully local/offline deployment | Fast cloud inference |



##  Observation:
Groq is faster, while Ollama allows fully offline usage. Both models remain grounded due to strict prompting.

## 🔍 QUALITY ANALYSIS

### Evaluation Questions
1. What services does Indecimal provide?
2. What makes Indecimal different from competitors?
3. How does Indecimal ensure construction quality?
4. What factors affect construction project delays?
5. Does Indecimal provide warranties?
6. What is included in the premium package?
7. How does Indecimal track project progress?
8. What happens if construction deviates from plan?
9. Does Indecimal support custom designs?
10. How can customers communicate with project managers?
11. What payment methods are accepted?
12. What is covered under standard packages?

---

### Evaluation Results

| Metric | Result |
|------|-------|
| Questions Tested | 12 |
| Relevant Retrieval | 11 / 12 |
| Hallucinations Observed | 0 |
| Complete Answers | 10 / 12 |
| Partial Answers | 2 / 12 |

---

### Observations

- Most retrieved chunks were highly relevant.
- No hallucinated answers were observed.
- Ollama produced grounded answers when context was available.
- When information was missing, the system correctly returned:




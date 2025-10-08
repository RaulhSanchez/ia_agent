import requests
from bs4 import BeautifulSoup
import faiss
import numpy as np
import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter

# Inicializar modelo y embeddings
llm = OllamaLLM(model="mistral")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Inicializar FAISS
index = faiss.IndexFlatL2(384)
vector_store = {}


def scrape_website(url):
    """Extrae texto de un sitio web"""
    try:
        st.write(f"🌐 Scraping website: {url}")
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return f"❌ Failed to fetch: {url}"

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text() for p in paragraphs)
        return text[:5000]

    except Exception as e:
        return f"⚠️ Error: {str(e)}"


def store_in_faiss(text, url):
    """Divide el texto, crea embeddings y los guarda en FAISS"""
    global index, vector_store
    st.write("💾 Storing data in FAISS...")

    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    texts = splitter.split_text(text)

    vectors = embeddings.embed_documents(texts)
    vectors = np.array(vectors, dtype=np.float32)

    index.add(vectors)
    start_id = len(vector_store)
    for i, chunk in enumerate(texts):
        vector_store[start_id + i] = (url, chunk)

    return "✅ Data stored successfully."


def retrieve_and_answer(query):
    """Recupera texto relevante y genera una respuesta con el modelo"""
    global index, vector_store

    query_vector = np.array(embeddings.embed_query(query), dtype=np.float32).reshape(1, -1)
    D, I = index.search(query_vector, k=2)

    context = ""
    for idx in I[0]:
        if idx in vector_store:
            context += vector_store[idx][1] + "\n\n"

    if not context:
        return "⚠️ No relevant data found."

    return llm.invoke(f"Based on the following context, answer the question:\n\n{context}\n\nQuestion: {query}\nAnswer:")


# --- Streamlit UI ---
st.title("🧠 IA Web Scraper con FAISS y Ollama")
st.write("Extrae, almacena y consulta información de una página web usando IA local.")

url = st.text_input("🔗 Introduce una URL web:")
if url:
    content = scrape_website(url)

    if "Failed" in content or "Error" in content:
        st.error(content)
    else:
        store_message = store_in_faiss(content, url)
        st.success(store_message)

query = st.text_input("💬 Haz una pregunta sobre el contenido:")
if query:
    answer = retrieve_and_answer(query)
    st.subheader("🤖 Respuesta de la IA:")
    st.write(answer)

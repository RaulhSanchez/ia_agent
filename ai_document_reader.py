import streamlit as st
import faiss
import numpy as np
import PyPDF2
from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter

# --- Inicialización ---
llm = OllamaLLM(model="mistral")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

index = faiss.IndexFlatL2(384)
vector_store = {}
summary_text = ""

splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)


# --- Funciones ---
def extract_text_from_pdf(upload_file):
    """Extrae texto de un archivo PDF."""
    pdf_reader = PyPDF2.PdfReader(upload_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text


def store_in_faiss(text, filename):
    """Almacena los embeddings del texto en FAISS."""
    global index, vector_store
    st.write(f"📦 Storing document {filename} in FAISS...")

    texts = splitter.split_text(text)
    vectors = embeddings.embed_documents(texts)
    vectors = np.array(vectors, dtype=np.float32)

    index.add(vectors)
    vector_store[len(vector_store)] = (filename, text)

    return "✅ Document stored successfully."


def generate_summary(text):
    """Genera un resumen del texto usando el modelo IA."""
    global summary_text
    st.write("🧠 Generating AI Summary...")
    summary_text = llm.invoke(f"Summarize the following document:\n\n{text[:3000]}")
    return summary_text


def retrieve_and_answer(query):
    """Recupera texto relevante y genera una respuesta con el modelo."""
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


def download_summary():
    """Permite descargar el resumen generado."""
    if summary_text:
        st.download_button(
            label="⬇️ Download Summary",
            data=summary_text,
            file_name="IA_Summary.txt",
            mime="text/plain"
        )


# --- Interfaz Streamlit ---
st.title("📘 AI Document Reader & Q&A Bot")
st.write("Sube un PDF, genera un resumen y haz preguntas sobre su contenido.")

upload_file = st.file_uploader("📂 Upload a PDF document", type=["pdf"])
if upload_file:
    text = extract_text_from_pdf(upload_file)
    store_message = store_in_faiss(text, upload_file.name)
    st.write(store_message)

    summary = generate_summary(text)
    st.subheader("📝 AI Summary:")
    st.write(summary)

    download_summary()

query = st.text_input("💬 Ask a question about the document:")
if query:
    answer = retrieve_and_answer(query)
    st.subheader("🤖 AI Answer:")
    st.write(answer)

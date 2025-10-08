import streamlit as st
import speech_recognition as sr
import pyttsx3
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

# Inicializar modelo Ollama
llm = OllamaLLM(model='mistral')


if "chat_history" not in st.session_state:
    st.session_state.chat_history = ChatMessageHistory()

# Inicializar motor de voz
engine = pyttsx3.init()
engine.setProperty("rate", 160)

# Inicializar reconocimiento de voz
recognizer = sr.Recognizer()


def speak(text):
    """Convierte texto a voz"""
    engine.say(text)
    engine.runAndWait()



def listen():
    """Escucha al micrófono y devuelve texto"""
    with sr.Microphone() as source:
        print("🎤 Escuchando...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio, language="es-ES")
        print(f"🗣️ Dijiste: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("❌ No entendí, inténtalo de nuevo.")
        return ""
    except sr.RequestError:
        print("⚠️ Servicio de reconocimiento no disponible.")
        return ""


prompt = PromptTemplate(
    input_variables=["chat_history", "question"], 
    template="Previous conversation:\n{chat_history}\nUser: {question}\nAI:"
)


def run_chain(question):
    chat_history_text = "\n".join([f"{msg.type.capitalize()}: {msg.content}" for msg in st.session_state.chat_history.messages])

    response = llm.invoke(prompt.format(chat_history=chat_history_text, question=question))

    st.session_state.chat_history.add_user_message(question)
    st.session_state.chat_history.add_ai_message(response)

    return response

st.title('IA chat con memoria')
st.write('pregunta')

if st.button('start listening'):
    user_query = listen()
    if user_query:
        ai_response = run_chain(user_query)
        st.write(f"YOU: {user_query}")
        st.write(f"IA: {ai_response}")
        speak(ai_response)


st.subheader("Chat history")
for msg in st.session_state.chat_history.messages:
    st.write(f"{msg.type.capitalize()}: {msg.content}")



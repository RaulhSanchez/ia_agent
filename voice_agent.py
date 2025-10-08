import speech_recognition as sr
import pyttsx3
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

# Inicializar modelo Ollama
llm = OllamaLLM(model='mistral')

# Inicializar historial del chat
chat_history = ChatMessageHistory()

# Inicializar motor de voz
engine = pyttsx3.init()
engine.setProperty("rate", 150)

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


# Definir prompt
prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template="Conversación previa:\n{chat_history}\nUsuario: {question}\nIA:"
)


def run_chain(question):
    """Genera una respuesta usando el modelo y actualiza el historial"""
    chat_history_text = "\n".join(
        [f"{msg.type.capitalize()}: {msg.content}" for msg in chat_history.messages]
    )

    response = llm.invoke(prompt.format(chat_history=chat_history_text, question=question))

    chat_history.add_user_message(question)
    chat_history.add_ai_message(response)

    return response


# Comienza el asistente
speak("Hola, soy tu asistente de voz con inteligencia artificial.")
print("👋 Di algo para empezar. Di 'salir' para terminar.")

while True:
    query = listen()
    if "salir" in query or "stop" in query:
        speak("Adiós 👋")
        break
    if query:
        response = run_chain(query)
        print(f"🤖 IA: {response}")
        speak(str(response))

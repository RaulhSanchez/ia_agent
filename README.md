# IA Chat con Memoria y Voz 🎙️🤖

Este proyecto es un **asistente de inteligencia artificial con memoria** que combina:

- **Streamlit**: Interfaz web interactiva.
- **LangChain Ollama**: Modelo de lenguaje local `mistral`.
- **SpeechRecognition**: Reconocimiento de voz para convertir audio a texto.
- **pyttsx3**: Texto a voz para responder en audio.
- **Memoria del chat**: Guarda la conversación anterior y la usa para generar respuestas más coherentes.

---

## Funcionalidades

- Escucha tu voz y convierte tus preguntas en texto.
- Responde usando un modelo de lenguaje (`mistral`) y reproduce la respuesta en audio.
- Guarda todo el historial de conversación y lo muestra en la interfaz de Streamlit.
- Interfaz web sencilla con Streamlit para interactuar de manera visual y auditiva.

---

## Requisitos

- Python 3.10+
- macOS, Windows o Linux con micrófono disponible.
- Librerías de Python:



```bash
pip install streamlit SpeechRecognition pyttsx3 langchain_ollama
```
En macOS puede ser necesario instalar PortAudio para que pyaudio funcione:

brew install portaudio
pip install pyaudio

## Uso

Clona el repositorio:
```bash
git clone https://github.com/tu_usuario/ia-chat-voz.git
cd ia-chat-voz
```

## Ejecuta la aplicación:

- streamlit run voice_chat_app.py


- Haz clic en Start Listening para comenzar a hablar con la IA.

- La IA responderá en voz y mostrará la respuesta en pantalla.

- El historial de conversación se mostrará en la sección Chat History.

## Estructura del proyecto
```bash
voice_chat_app.py       # Script principal
README.md               # Documentación
requirements.txt        # Opcional, con librerías necesarias
```
- Configuración del reconocimiento de voz y motor TTS

- Reconocimiento de voz: SpeechRecognition captura audio desde el micrófono y lo convierte en texto usando la API de Google.

- Motor de voz: pyttsx3 reproduce las respuestas de la IA en audio.

- Memoria del chat: ChatMessageHistory de LangChain guarda la conversación durante la sesión de Streamlit.

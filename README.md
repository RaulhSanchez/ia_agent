# 🤖 IA Projects Suite — Chat, Web Scraper & Document Reader

Este repositorio reúne **tres aplicaciones de inteligencia artificial** construidas con **Streamlit**, **LangChain**, **Ollama** y modelos locales como `mistral`.

Incluye:

- 🎙️ **IA Chat con Voz y Memoria**
- 🌐 **IA Web Scraper con FAISS**
- 📘 **IA Document Reader & Q&A Bot**

Cada herramienta aprovecha el poder del lenguaje natural para procesar texto, voz y documentos.

---

## 🧩 Tecnologías principales

- **Python 3.10+**
- **Streamlit** — Interfaz web interactiva.
- **LangChain + Ollama (Mistral)** — Lógica de IA y razonamiento local.
- **SpeechRecognition + pyttsx3** — Reconocimiento y síntesis de voz.
- **FAISS** — Motor de búsqueda semántica vectorial.
- **BeautifulSoup** — Scraping de sitios web.
- **PyPDF2** — Lectura de documentos PDF.

---

## ⚙️ Instalación general

```bash
pip install streamlit SpeechRecognition pyttsx3 langchain_ollama beautifulsoup4 faiss-cpu PyPDF2

```
En macOS puede ser necesario instalar PortAudio para que pyaudio funcione:

brew install portaudio
pip install pyaudio

## Uso Chat voz

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
ai_docuemnt_reader.py   # Script principal
ai_scraper_web_fais.py   # Script principal
README.md               # Documentación
```
- Configuración del reconocimiento de voz y motor TTS

- Reconocimiento de voz: SpeechRecognition captura audio desde el micrófono y lo convierte en texto usando la API de Google.

- Motor de voz: pyttsx3 reproduce las respuestas de la IA en audio.

- Memoria del chat: ChatMessageHistory de LangChain guarda la conversación durante la sesión de Streamlit.


- Extrae texto de PDFs con PyPDF2.

- Genera un resumen con IA.

- Guarda embeddings en FAISS para consultas semánticas.

- Responde preguntas sobre el documento.

- Permite descargar el resumen generado.




- Scrapea una web con BeautifulSoup.

- Resume el contenido con Mistral.

- Guarda los embeddings en FAISS.

- Permite realizar preguntas sobre el contenido de la web

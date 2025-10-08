import requests
from bs4 import BeautifulSoup
import streamlit as st
from langchain_ollama import OllamaLLM

# Inicializar modelo Ollama
llm = OllamaLLM(model='mistral')


def scrape_website(url):
    try:
        st.write(f"Scraping website: {url}")
        headers= {"User-Agent":"Mozila/5.0"}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return f"failed to fetch: {url}"     

        soup  = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text() for p in paragraphs)

        return text[:2000]
    
    except Exception as e:
        return f"Error: {str(e)}"   


def sumarize_content(content):
    st.write("Summarizing content")
    return llm.invoke(f"Summarize the following content:\n\n{content[:1000]}")

st.title('IA Powered web scraper')
st.write('Enter web URL')

url = st.text_input("enter web url:")
if url:
    content = scrape_website(url)

    if "Failed" in content or "Error" in content:
        st.write(content)
    else:
        summary = sumarize_content(content)
        st.subheader("Web Summary")
        st.write(summary)
       
# Agente IA basico con memoria e interfaz web

import streamlit as st
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model='mistral')


if "chat_history" not in st.session_state:
    st.session_state.chat_history = ChatMessageHistory()

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

# StreamLit interface

st.title('IA chat con memoria')
st.write('pregunta')

user_input = st.text_input('Tu pregunta:')
if user_input:
    response = run_chain(user_input)
    st.write(f"YOU: {user_input}")
    st.write(f"IA: {response}")


st.subheader("Chat history")
for msg in st.session_state.chat_history.messages:
    st.write(f"{msg.type.capitalize()}: {msg.content}")

    





# Agente IA basico con memoria


# from langchain_community.chat_message_histories import ChatMessageHistory
# from langchain_core.prompts import PromptTemplate
# from langchain_ollama import OllamaLLM

# llm = OllamaLLM(model='mistral')

# # inicializar memoria del chat
# chat_history = ChatMessageHistory()

# prompt = PromptTemplate(
#     input_variables=["chat_history", "question"], 
#     template="Previous conversation:\n{chat_history}\nUser: {question}\nAI:"
# )

# def run_chain(question):
#     chat_history_text = "\n".join([f"{msg.type.capitalize()}: {msg.content}" for msg in chat_history.messages])

#     response = llm.invoke(prompt.format(chat_history=chat_history_text, question=question))

#     chat_history.add_user_message(question)
#     chat_history.add_ai_message(response)

#     return response

# print("\nAI chat bot con memoria")    
# print("Escribe 'exit' para salir")

# while True:
#     user_input = input("\nYou: ")
#     if user_input.lower() == 'exit':
#         print('Adiós')
#         break
#     ai_response = run_chain(user_input)
#     print(f"AI: {ai_response}")





# Agente IA basico



# from langchain_ollama import OllamaLLM

# llm = OllamaLLM(model='mistral')

# while True:
#     question = input("Your question: ")
#     if question.lower() == 'exit':
#         print('adios')
#         break
#     response = llm.invoke(question)
#     print('response: ',response)


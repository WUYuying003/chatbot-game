import streamlit as st
import ollama

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by Ollama")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    try:
        response = ollama.chat(model="llama3.2:1b", messages=st.session_state.messages)
        msg = response['message']['content']
        st.chat_message("assistant").write(msg)
        st.session_state.messages.append({"role": "assistant", "content": msg})
    except Exception as e:
        error_msg = f"Error: {str(e)}\n\nPlease make sure Ollama is running and the model is installed:\n`ollama pull llama3.2:1b`"
        st.chat_message("assistant").write(error_msg)
        st.session_state.messages.append({"role": "assistant", "content": error_msg})

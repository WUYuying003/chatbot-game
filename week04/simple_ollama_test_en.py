import streamlit as st
import requests
import json

st.title("💬 Ollama Chatbot (Direct API)")
st.caption("🚀 Ollama chatbot using direct API calls")

def chat_with_ollama(message):
    """Communicate with Ollama directly through HTTP API"""
    try:
        url = "http://localhost:11434/api/chat"
        payload = {
            "model": "llama3.2:1b",
            "messages": [{"role": "user", "content": message}],
            "stream": False
        }
        
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result.get('message', {}).get('content', 'No response received')
        else:
            return f"Error: HTTP {response.status_code} - {response.text}"
    
    except requests.exceptions.ConnectionError:
        return "❌ Cannot connect to Ollama service. Please make sure Ollama is running on port 11434."
    except requests.exceptions.Timeout:
        return "❌ Request timeout. The model might be loading, please try again."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
if prompt := st.chat_input("Enter your message..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_with_ollama(prompt)
            st.write(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar with instructions
with st.sidebar:
    st.header("🛠️ Setup Instructions")
    st.code("""
# Start Ollama service
ollama serve

# Install model
ollama pull llama3.2:1b

# Check if running
curl http://localhost:11434/api/tags
    """)
    
    st.header("ℹ️ About")
    st.write("""
    This chatbot uses direct HTTP API calls to communicate with Ollama,
    providing a more stable connection than the Python package.
    """)
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.experimental_rerun()
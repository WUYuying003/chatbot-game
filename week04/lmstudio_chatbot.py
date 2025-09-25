import streamlit as st
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by LMStudio")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    try:
        response = client.chat.completions.create(
            model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
            messages=st.session_state.messages,
            stream=True,
        )

        msg = ""

        def stream_response():
            global msg
            for chunk in response:
                try:
                    part = chunk.choices[0].delta.content
                    if part:
                        msg += part
                        yield part
                except:
                    continue

        
        st.chat_message("assistant").write_stream(stream_response)
        
        st.session_state.messages.append({"role": "assistant", "content": msg})
        
    except Exception as e:
        error_msg = f"❌ 连接LM Studio失败: {str(e)}\n\n请确保:\n1. LM Studio已安装并启动\n2. 已加载模型\n3. 本地服务器在端口1234运行\n\n或者尝试使用Ollama聊天机器人。"
        st.chat_message("assistant").write(error_msg)
        st.session_state.messages.append({"role": "assistant", "content": error_msg})

import streamlit as st
import requests
import json

st.title("💬 Ollama 聊天机器人 (直接API)")
st.caption("🚀 使用直接API调用的Ollama聊天机器人")

def chat_with_ollama(message):
    """直接通过HTTP API与Ollama通信"""
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
            return result['message']['content']
        else:
            return f"错误: HTTP {response.status_code} - {response.text}"
            
    except requests.exceptions.ConnectionError:
        return "❌ 连接错误: 无法连接到Ollama服务器 (localhost:11434)"
    except requests.exceptions.Timeout:
        return "⏱️ 超时错误: 请求超时，请稍后重试"
    except Exception as e:
        return f"❌ 未知错误: {str(e)}"

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "你好！我是Ollama AI助手，有什么可以帮你的吗？"}]

# 显示聊天历史
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 用户输入
if prompt := st.chat_input("请输入你的问题..."):
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # 显示"正在思考"的状态
    with st.chat_message("assistant"):
        with st.spinner("正在思考..."):
            response = chat_with_ollama(prompt)
        st.write(response)
    
    # 添加助手回复到会话
    st.session_state.messages.append({"role": "assistant", "content": response})
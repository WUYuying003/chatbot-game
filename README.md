# 🎮 AI聊天机器人 + 俄罗斯方块

个人项目：集成AI聊天功能和俄罗斯方块游戏的网页应用

## 🚀 快速开始

```bash
# 安装依赖
pip install streamlit requests ollama pygame

# 启动Ollama服务
ollama serve
ollama pull llama3.2:1b

# 运行集成版应用
streamlit run week04/chatbot_with_tetris.py

# 或运行独立版游戏
python tetris_game.py
```

## ✨ 功能特色

- 🤖 AI聊天助手（支持游戏数据分析）
- 🎮 完整俄罗斯方块游戏（支持暂停）
- 📊 自动游戏历史记录
- 💬 智能统计查询

## 🎯 操作说明

### 游戏控制
- `←→` 移动 | `↑` 旋转 | `↓` 加速 | `空格` 硬降 | `P` 暂停

### AI助手
询问游戏表现："我的游戏记录怎么样？"

---
作者: WUYuying003
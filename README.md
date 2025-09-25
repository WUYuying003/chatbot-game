# 🎮 AI Chatbot + Tetris Game

Personal project: Web application integrating AI chat functionality with Tetris game

## 🚀 Quick Start

```bash
# Install dependencies
pip install streamlit requests ollama pygame

# Start Ollama service
ollama serve
ollama pull llama3.2:1b

# Run integrated application
streamlit run week04/chatbot_with_tetris.py

# Or run standalone game
python tetris_game.py
```

## ✨ Features

- 🤖 AI Chat Assistant (supports game data analysis)
- 🎮 Complete Tetris game (with pause function)
- 📊 Automatic game history recording
- 💬 Intelligent statistics queries

## 🎯 Instructions

### Game Controls
- `←→` Move | `↑` Rotate | `↓` Speed up | `Space` Hard drop | `P` Pause

### AI Assistant
Ask about game performance: "How are my game records?"

## 📁 Project Structure

```
├── week04/
│   ├── chatbot_with_tetris.py     # Main integrated application
│   ├── simple_ollama_test_en.py   # Simple chatbot (English)
│   ├── ollama_chatbot.py          # Basic chatbot
│   └── requirements.txt           # Dependencies
├── tetris_game.py                 # Standalone Tetris game (Pygame)
├── requirements.txt               # Main dependencies
└── README.md                      # Project documentation
```

## 🛠️ Technical Stack

- **Frontend**: Streamlit + HTML5 Canvas
- **Backend**: Python
- **AI Model**: Ollama (llama3.2:1b)
- **Game Engine**: HTML5 Canvas (web) + Pygame (standalone)
- **Data Storage**: Browser LocalStorage

## 🎨 Key Features

1. **Dual-column layout**: Chat on left, game on right, no interference
2. **Smart data analysis**: AI understands and analyzes your game performance
3. **Pause function**: Supports pausing and resuming game anytime
4. **History records**: Automatically saves and queryable game history
5. **Responsive design**: Adapts to different screen sizes

---
Author: WUYuying003  
Contact: 25056092g@connect.polyu.hk
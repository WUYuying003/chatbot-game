# Week 04 Assignment: AI Chatbot Integration

## Project Overview

This project demonstrates the integration of an AI chatbot with an interactive Tetris game using Streamlit framework. The application showcases advanced web development skills combining multiple technologies.

## Technical Implementation

### Architecture
- **Frontend**: Streamlit web framework with HTML5 Canvas for game rendering
- **Backend**: Python with direct HTTP API calls to Ollama service
- **AI Integration**: Ollama LLM (llama3.2:1b model) for intelligent conversations
- **Game Logic**: JavaScript-based Tetris implementation with full game mechanics

### Key Components

1. **AI Chatbot System**
   - Direct HTTP API integration with Ollama service
   - Context-aware conversations with game data analysis
   - Robust error handling and user feedback
   - Session state management for chat history

2. **Tetris Game Engine**
   - Complete implementation of classic Tetris gameplay
   - 7 different tetromino shapes with rotation mechanics
   - Line clearing algorithm with score calculation
   - Level progression system
   - Pause/resume functionality

3. **Data Management**
   - Automatic game statistics recording
   - Local storage for persistent data
   - Real-time performance analytics
   - Historical data querying through AI assistant

## Features Implemented

### Core Functionality
- ✅ Real-time AI chat interface
- ✅ Complete Tetris game with all standard mechanics
- ✅ Dual-column responsive layout
- ✅ Game data recording and analysis
- ✅ Intelligent statistics queries via AI

### Advanced Features
- ✅ Pause/resume game functionality (P key)
- ✅ Hard drop and soft drop controls
- ✅ Level progression with increasing speed
- ✅ Game history with detailed statistics
- ✅ Context-aware AI responses about game performance

## Code Quality & Best Practices

### Python Backend
- Modular code structure with clear separation of concerns
- Comprehensive error handling for API connections
- Session state management for data persistence
- Type hints and documentation

### Frontend Implementation
- Responsive design using Streamlit columns
- Clean HTML/CSS for game rendering
- Efficient JavaScript game loop
- Cross-browser compatibility

### API Integration
- Direct HTTP calls for better reliability than Python packages
- Timeout handling and connection error management
- Structured JSON communication with Ollama service

## Installation & Setup

### Prerequisites
```bash
# Install required packages
pip install streamlit requests ollama pygame

# Setup Ollama service
ollama serve
ollama pull llama3.2:1b
```

### Running the Application
```bash
# Main integrated application
streamlit run week04/chatbot_with_tetris.py

# Simple chatbot version
streamlit run week04/simple_ollama_test_en.py

# Standalone game
python tetris_game.py
```

## User Experience

### Game Controls
- **Arrow Keys**: Move (←→), Rotate (↑), Speed up (↓)
- **Spacebar**: Hard drop
- **P Key**: Pause/Resume
- **Buttons**: New Game, Pause/Resume, View History

### AI Interaction
Users can ask about their gaming performance:
- "How are my game statistics?"
- "What's my highest score?"
- "Show my recent games"
- "Analyze my performance"

## Technical Challenges Solved

1. **API Reliability**: Solved Ollama Python package connection issues by implementing direct HTTP API calls
2. **Game State Management**: Implemented proper pause/resume functionality with visual feedback
3. **Data Persistence**: Created browser-based local storage for game history
4. **Real-time Updates**: Synchronized game data with AI assistant for intelligent analysis
5. **Cross-platform Compatibility**: Ensured consistent performance across different systems

## Learning Outcomes

- Advanced Streamlit framework usage
- Integration of multiple technologies (Python, JavaScript, HTML5 Canvas)
- API design and implementation
- Game development fundamentals
- User experience design
- Error handling and debugging

## Future Enhancements

- Multiplayer functionality
- Advanced AI analysis with machine learning insights
- Mobile-responsive controls
- Leaderboard system
- Custom game themes

---

**Student**: WUYuying003  
**Email**: 25056092g@connect.polyu.hk  
**Course**: Week 04 - Advanced Web Applications  
**Submission Date**: September 26, 2025
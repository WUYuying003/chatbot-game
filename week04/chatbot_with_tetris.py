import streamlit as st
import requests
import json
import streamlit.components.v1 as components

st.set_page_config(
    page_title="AI Chatbot + Tetris Game", 
    page_icon="🎮", 
    layout="wide"
)

# 俄罗斯方块HTML游戏代码
tetris_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; padding: 20px; font-family: Arial, sans-serif; }
        .game-container { 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            flex-direction: column;
        }
        canvas { 
            border: 2px solid #333; 
            background: #000;
        }
        .info { 
            margin: 10px; 
            text-align: center;
            color: #333;
        }
        .controls {
            margin: 10px;
            text-align: center;
            color: #666;
            font-size: 14px;
        }
        .pause-overlay {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 20px;
            border-radius: 10px;
            font-size: 24px;
            display: none;
        }
        button {
            margin: 5px;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
        }
        button:hover {
            background: #45a049;
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h2>🎮 Tetris Game</h2>
        <div class="info">
            <span>Score: <span id="score">0</span></span> | 
            <span>Level: <span id="level">1</span></span> | 
            <span>Lines: <span id="lines">0</span></span>
        </div>
        <div style="position: relative;">
            <canvas id="tetris" width="300" height="600"></canvas>
            <div id="pauseOverlay" class="pause-overlay">Game Paused<br>Press P to Continue</div>
        </div>
        <div class="controls">
            <div>Controls: ←→ Move | ↑ Rotate | ↓ Speed Up | Space Hard Drop | P Pause</div>
            <button onclick="newGame()">New Game</button>
            <button onclick="togglePause()">Pause/Resume</button>
            <button onclick="showHistory()">View History</button>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('tetris');
        const context = canvas.getContext('2d');
        
        const ROWS = 20;
        const COLS = 10;
        const BLOCK_SIZE = 30;
        
        let board = Array(ROWS).fill().map(() => Array(COLS).fill(0));
        let score = 0;
        let level = 1;
        let linesCleared = 0;
        let dropCounter = 0;
        let dropInterval = 1000;
        let lastTime = 0;
        let gameOver = false;
        let paused = false;
        let gameStartTime = Date.now();
        
        const colors = [
            null,
            '#FF0D72', '#0DC2FF', '#0DFF72',
            '#F538FF', '#FF8E0D', '#FFE138', '#3877FF'
        ];
        
        const pieces = [
            [[[1,1,1,1]]],  // I
            [[[2,2],[2,2]]],  // O
            [[[0,3,0],[3,3,3]], [[3,0],[3,3],[3,0]], [[3,3,3],[0,3,0]], [[0,3],[3,3],[0,3]]],  // T
            [[[0,4,4],[4,4,0]], [[4,0],[4,4],[0,4]]],  // S
            [[[5,5,0],[0,5,5]], [[0,5],[5,5],[5,0]]],  // Z
            [[[6,0,0],[6,6,6]], [[6,6],[6,0],[6,0]], [[6,6,6],[0,0,6]], [[0,6],[0,6],[6,6]]],  // J
            [[[0,0,7],[7,7,7]], [[7,0],[7,0],[7,7]], [[7,7,7],[7,0,0]], [[7,7],[0,7],[0,7]]]   // L
        ];
        
        let currentPiece = {
            shape: null,
            x: 0,
            y: 0,
            rotation: 0
        };
        
        function getRandomPiece() {
            const pieceType = Math.floor(Math.random() * pieces.length);
            return {
                shape: pieces[pieceType],
                x: Math.floor(COLS / 2) - 1,
                y: 0,
                rotation: 0
            };
        }
        
        function drawBlock(x, y, color) {
            context.fillStyle = colors[color] || '#333';
            context.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
            context.strokeStyle = '#fff';
            context.strokeRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
        }
        
        function drawBoard() {
            context.clearRect(0, 0, canvas.width, canvas.height);
            for (let row = 0; row < ROWS; row++) {
                for (let col = 0; col < COLS; col++) {
                    if (board[row][col]) {
                        drawBlock(col, row, board[row][col]);
                    }
                }
            }
        }
        
        function drawPiece() {
            if (!currentPiece.shape) return;
            const shape = currentPiece.shape[currentPiece.rotation];
            for (let row = 0; row < shape.length; row++) {
                for (let col = 0; col < shape[row].length; col++) {
                    if (shape[row][col]) {
                        drawBlock(currentPiece.x + col, currentPiece.y + row, shape[row][col]);
                    }
                }
            }
        }
        
        function isValidMove(piece, dx = 0, dy = 0, rotation = piece.rotation) {
            const shape = piece.shape[rotation];
            for (let row = 0; row < shape.length; row++) {
                for (let col = 0; col < shape[row].length; col++) {
                    if (shape[row][col]) {
                        const newX = piece.x + col + dx;
                        const newY = piece.y + row + dy;
                        if (newX < 0 || newX >= COLS || newY >= ROWS || 
                            (newY >= 0 && board[newY][newX])) {
                            return false;
                        }
                    }
                }
            }
            return true;
        }
        
        function placePiece() {
            const shape = currentPiece.shape[currentPiece.rotation];
            for (let row = 0; row < shape.length; row++) {
                for (let col = 0; col < shape[row].length; col++) {
                    if (shape[row][col]) {
                        const boardY = currentPiece.y + row;
                        const boardX = currentPiece.x + col;
                        if (boardY >= 0) {
                            board[boardY][boardX] = shape[row][col];
                        }
                    }
                }
            }
        }
        
        function clearLines() {
            let linesRemoved = 0;
            for (let row = ROWS - 1; row >= 0; row--) {
                if (board[row].every(cell => cell !== 0)) {
                    board.splice(row, 1);
                    board.unshift(Array(COLS).fill(0));
                    linesRemoved++;
                    row++;
                }
            }
            
            if (linesRemoved > 0) {
                linesCleared += linesRemoved;
                score += linesRemoved * 100 * level;
                level = Math.floor(linesCleared / 10) + 1;
                dropInterval = Math.max(100, 1000 - (level - 1) * 100);
                updateDisplay();
            }
        }
        
        function updateDisplay() {
            document.getElementById('score').textContent = score;
            document.getElementById('level').textContent = level;
            document.getElementById('lines').textContent = linesCleared;
        }
        
        function newGame() {
            board = Array(ROWS).fill().map(() => Array(COLS).fill(0));
            score = 0;
            level = 1;
            linesCleared = 0;
            dropInterval = 1000;
            gameOver = false;
            paused = false;
            gameStartTime = Date.now();
            currentPiece = getRandomPiece();
            updateDisplay();
            document.getElementById('pauseOverlay').style.display = 'none';
        }
        
        function togglePause() {
            paused = !paused;
            const overlay = document.getElementById('pauseOverlay');
            if (paused) {
                overlay.style.display = 'block';
            } else {
                overlay.style.display = 'none';
            }
        }
        
        function saveGameData() {
            const gameData = {
                score: score,
                level: level,
                lines: linesCleared,
                timestamp: new Date().toLocaleString('zh-CN'),
                duration: Math.floor((Date.now() - gameStartTime) / 1000)
            };
            
            // 保存到localStorage作为备用方案
            let gameHistory = JSON.parse(localStorage.getItem('tetrisHistory') || '[]');
            gameHistory.push(gameData);
            // 只保留最近20场游戏
            if (gameHistory.length > 20) {
                gameHistory = gameHistory.slice(-20);
            }
            localStorage.setItem('tetrisHistory', JSON.stringify(gameHistory));
            
            console.log('游戏数据已保存:', gameData);
        }
        
        function showHistory() {
            const history = JSON.parse(localStorage.getItem('tetrisHistory') || '[]');
            if (history.length === 0) {
                alert('No game history available');
                return;
            }
            
            let historyText = '🎮 Game History:\\n\\n';
            history.slice(-5).reverse().forEach((game, index) => {
                historyText += `${index + 1}. ${game.timestamp}\\n   Score: ${game.score.toLocaleString()} | Level: ${game.level} | Lines: ${game.lines} | Duration: ${game.duration}s\\n\\n`;
            });
            
            alert(historyText);
        }
        
        function gameLoop(time = 0) {
            if (!paused && !gameOver) {
                const deltaTime = time - lastTime;
                dropCounter += deltaTime;
                
                if (dropCounter > dropInterval) {
                    if (isValidMove(currentPiece, 0, 1)) {
                        currentPiece.y++;
                    } else {
                        placePiece();
                        clearLines();
                        currentPiece = getRandomPiece();
                        
                        if (!isValidMove(currentPiece)) {
                            gameOver = true;
                            saveGameData(); // 保存游戏数据
                            alert('Game Over! Score: ' + score + '\\nGame Duration: ' + Math.floor((Date.now() - gameStartTime) / 1000) + ' seconds');
                        }
                    }
                    dropCounter = 0;
                }
            }
            
            lastTime = time;
            drawBoard();
            drawPiece();
            requestAnimationFrame(gameLoop);
        }
        
        document.addEventListener('keydown', (e) => {
            if (gameOver || paused) return;
            
            switch(e.code) {
                case 'ArrowLeft':
                    if (isValidMove(currentPiece, -1, 0)) {
                        currentPiece.x--;
                    }
                    break;
                case 'ArrowRight':
                    if (isValidMove(currentPiece, 1, 0)) {
                        currentPiece.x++;
                    }
                    break;
                case 'ArrowDown':
                    if (isValidMove(currentPiece, 0, 1)) {
                        currentPiece.y++;
                        score += 1;
                        updateDisplay();
                    }
                    break;
                case 'ArrowUp':
                    const newRotation = (currentPiece.rotation + 1) % currentPiece.shape.length;
                    if (isValidMove(currentPiece, 0, 0, newRotation)) {
                        currentPiece.rotation = newRotation;
                    }
                    break;
                case 'Space':
                    while (isValidMove(currentPiece, 0, 1)) {
                        currentPiece.y++;
                        score += 2;
                    }
                    updateDisplay();
                    break;
                case 'KeyP':
                    togglePause();
                    break;
            }
        });
        
        // 初始化游戏
        newGame();
        gameLoop();
    </script>
</body>
</html>
"""

# Page layout
st.title("🎮 AI Chatbot + Tetris Game")
st.caption("🚀 Dual experience of chatting and gaming")

# Create two-column layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("💬 AI Assistant")
    
    # Initialize game history data
    if "game_history" not in st.session_state:
        st.session_state["game_history"] = []
    
    # Chatbot logic
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Hello! I'm an AI Gaming Assistant. I can:\n\n🎮 Record your Tetris game data\n📊 Analyze your gaming performance\n💬 Answer any questions\n\nStart playing! I'll automatically record your scores."}]

    # Display chat history
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # User input
    if prompt := st.chat_input("Please enter your question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        # Check if query is game data related
        game_keywords = ["game", "score", "history", "record", "statistics", "performance", "tetris", "stats"]
        if any(keyword.lower() in prompt.lower() for keyword in game_keywords) and st.session_state.game_history:
            # Generate game statistics report
            total_games = len(st.session_state.game_history)
            if total_games > 0:
                avg_score = sum(game['score'] for game in st.session_state.game_history) / total_games
                max_score = max(game['score'] for game in st.session_state.game_history)
                max_level = max(game['level'] for game in st.session_state.game_history)
                total_lines = sum(game['lines'] for game in st.session_state.game_history)
                
                stats_msg = f"""📊 **Your Tetris Game Statistics:**

🎮 **Total Games Played:** {total_games} games
🏆 **Highest Score:** {max_score:,} points
📈 **Average Score:** {avg_score:,.0f} points  
⭐ **Highest Level Reached:** {max_level}
📏 **Total Lines Cleared:** {total_lines} lines

📋 **Recent 5 Games:**"""
                
                # Show recent 5 games
                recent_games = st.session_state.game_history[-5:]
                for i, game in enumerate(reversed(recent_games), 1):
                    stats_msg += f"\n{i}. {game['timestamp']} - Score: {game['score']:,} | Level: {game['level']} | Lines: {game['lines']} | Duration: {game['duration']}s"
                
                st.chat_message("assistant").write(stats_msg)
                st.session_state.messages.append({"role": "assistant", "content": stats_msg})
        else:
            try:
                # Use direct HTTP API to call Ollama
                url = "http://localhost:11434/api/chat"
                
                # Add game history to context if available
                context_message = ""
                if st.session_state.game_history:
                    recent_stats = f"User's recent gaming stats: Played {len(st.session_state.game_history)} games total, highest score {max(game['score'] for game in st.session_state.game_history)} points."
                    context_message = recent_stats
                
                messages_with_context = st.session_state.messages.copy()
                if context_message:
                    messages_with_context.insert(-1, {"role": "system", "content": context_message})
                
                data = {
                    "model": "llama3.2:1b",
                    "messages": messages_with_context,
                    "stream": False
                }
                
                response = requests.post(url, json=data, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    msg = result.get('message', {}).get('content', 'Sorry, no valid response received.')
                    st.chat_message("assistant").write(msg)
                    st.session_state.messages.append({"role": "assistant", "content": msg})
                else:
                    error_msg = f"❌ API call failed (Status code: {response.status_code})\n\nPlease ensure Ollama is running:\n1. Run in terminal: `ollama serve`\n2. Confirm model is installed: `ollama pull llama3.2:1b`"
                    st.chat_message("assistant").write(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    
            except requests.exceptions.ConnectionError:
                error_msg = "❌ Cannot connect to Ollama service\n\nPlease check:\n1. Is Ollama running? Run command: `ollama serve`\n2. Is the service running on port 11434?"
                st.chat_message("assistant").write(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
            except requests.exceptions.Timeout:
                error_msg = "❌ Request timeout\n\nThe model might be loading, please try again later."
                st.chat_message("assistant").write(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
            except Exception as e:
                error_msg = f"❌ Error occurred: {str(e)}\n\nPlease check Ollama service status."
                st.chat_message("assistant").write(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

with col2:
    st.header("🎮 Tetris Game")
    
    # Add game history sidebar
    if st.session_state.game_history:
        with st.expander("📊 Game History", expanded=False):
            st.write(f"**Total Games Played:** {len(st.session_state.game_history)}")
            if len(st.session_state.game_history) > 0:
                max_score = max(game['score'] for game in st.session_state.game_history)
                avg_score = sum(game['score'] for game in st.session_state.game_history) / len(st.session_state.game_history)
                st.write(f"**Highest Score:** {max_score:,}")
                st.write(f"**Average Score:** {avg_score:.0f}")
                
                st.write("**Recent Games:**")
                recent_games = st.session_state.game_history[-5:]
                for game in reversed(recent_games):
                    st.write(f"🕒 {game['timestamp']} - Score: {game['score']:,} | Level: {game['level']} | Lines: {game['lines']}")
    
    # Embed Tetris game
    components.html(tetris_html, height=750)

# Add instructions
st.markdown("---")
st.markdown("""
### 🎯 Usage Instructions:
- **Left Chat Area**: Chat with AI assistant, ask any questions
- **Right Game Area**: Enjoy the classic Tetris game
- **Game Controls**: Use arrow keys to control blocks, spacebar for hard drop
- **Multitasking**: Chat and play simultaneously without interference!

### 🚀 Key Features:
- 🤖 Intelligent AI conversation assistant
- 🎮 Complete Tetris game experience
- 📱 Responsive design for all screen sizes
- ⚡ Real-time gaming experience
""")
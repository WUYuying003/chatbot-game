import streamlit as st
import requests
import json
import streamlit.components.v1 as components

st.set_page_config(
    page_title="AI聊天机器人 + 俄罗斯方块", 
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
        <h2>🎮 俄罗斯方块</h2>
        <div class="info">
            <span>分数: <span id="score">0</span></span> | 
            <span>等级: <span id="level">1</span></span> | 
            <span>消行: <span id="lines">0</span></span>
        </div>
        <div style="position: relative;">
            <canvas id="tetris" width="300" height="600"></canvas>
            <div id="pauseOverlay" class="pause-overlay">游戏已暂停<br>按P继续</div>
        </div>
        <div class="controls">
            <div>操作: ←→移动 | ↑旋转 | ↓加速 | 空格硬降 | P暂停</div>
            <button onclick="newGame()">新游戏</button>
            <button onclick="togglePause()">暂停/继续</button>
            <button onclick="showHistory()">查看历史</button>
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
                alert('暂无游戏历史记录');
                return;
            }
            
            let historyText = '🎮 游戏历史记录:\\n\\n';
            history.slice(-5).reverse().forEach((game, index) => {
                historyText += `${index + 1}. ${game.timestamp}\\n   分数: ${game.score.toLocaleString()} | 等级: ${game.level} | 消行: ${game.lines} | 时长: ${game.duration}秒\\n\\n`;
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
                            alert('游戏结束! 分数: ' + score + '\\n游戏时长: ' + Math.floor((Date.now() - gameStartTime) / 1000) + '秒');
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

# 页面布局
st.title("🎮 AI聊天机器人 + 俄罗斯方块")
st.caption("🚀 边聊天边游戏的双重体验")

# 创建两列布局
col1, col2 = st.columns([1, 1])

with col1:
    st.header("💬 AI聊天助手")
    
    # 初始化游戏历史数据
    if "game_history" not in st.session_state:
        st.session_state["game_history"] = []
    
    # 聊天机器人逻辑
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "你好！我是AI游戏助手。我可以：\n\n🎮 记录你的俄罗斯方块游戏数据\n📊 分析你的游戏表现\n💬 回答任何问题\n\n开始游戏吧！我会自动记录你的成绩。"}]

    # 显示聊天历史
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # 用户输入
    if prompt := st.chat_input("请输入你的问题..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        # 检查是否是游戏数据相关的查询
        game_keywords = ["游戏", "分数", "历史", "记录", "统计", "表现", "成绩", "俄罗斯方块"]
        if any(keyword in prompt for keyword in game_keywords) and st.session_state.game_history:
            # 生成游戏统计报告
            total_games = len(st.session_state.game_history)
            if total_games > 0:
                avg_score = sum(game['score'] for game in st.session_state.game_history) / total_games
                max_score = max(game['score'] for game in st.session_state.game_history)
                max_level = max(game['level'] for game in st.session_state.game_history)
                total_lines = sum(game['lines'] for game in st.session_state.game_history)
                
                stats_msg = f"""📊 **你的俄罗斯方块统计数据：**

🎮 **总游戏次数：** {total_games} 场
🏆 **最高分数：** {max_score:,} 分
📈 **平均分数：** {avg_score:,.0f} 分  
⭐ **最高等级：** {max_level} 级
📏 **总消除行数：** {total_lines} 行

📋 **最近5场游戏记录：**"""
                
                # 显示最近5场游戏
                recent_games = st.session_state.game_history[-5:]
                for i, game in enumerate(reversed(recent_games), 1):
                    stats_msg += f"\n{i}. {game['timestamp']} - 分数: {game['score']:,} | 等级: {game['level']} | 消行: {game['lines']} | 时长: {game['duration']}秒"
                
                st.chat_message("assistant").write(stats_msg)
                st.session_state.messages.append({"role": "assistant", "content": stats_msg})
        else:
            try:
                # 使用直接HTTP API调用Ollama
                url = "http://localhost:11434/api/chat"
                
                # 如果有游戏历史，添加到上下文中
                context_message = ""
                if st.session_state.game_history:
                    recent_stats = f"用户最近的游戏统计：总共玩了{len(st.session_state.game_history)}场，最高分{max(game['score'] for game in st.session_state.game_history)}分。"
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
                    msg = result.get('message', {}).get('content', '抱歉，没有收到有效回复。')
                    st.chat_message("assistant").write(msg)
                    st.session_state.messages.append({"role": "assistant", "content": msg})
                else:
                    error_msg = f"❌ API调用失败 (状态码: {response.status_code})\n\n请确保Ollama正在运行：\n1. 在终端运行: `ollama serve`\n2. 确认模型已安装: `ollama pull llama3.2:1b`"
                    st.chat_message("assistant").write(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    
            except requests.exceptions.ConnectionError:
                error_msg = "❌ 无法连接到Ollama服务\n\n请检查：\n1. Ollama是否正在运行？运行命令: `ollama serve`\n2. 服务是否在端口11434运行？"
                st.chat_message("assistant").write(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
            except requests.exceptions.Timeout:
                error_msg = "❌ 请求超时\n\n模型可能正在加载中，请稍后再试。"
                st.chat_message("assistant").write(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
            except Exception as e:
                error_msg = f"❌ 发生错误: {str(e)}\n\n请检查Ollama服务状态。"
                st.chat_message("assistant").write(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

with col2:
    st.header("🎮 俄罗斯方块")
    
    # 添加游戏历史侧边栏
    if st.session_state.game_history:
        with st.expander("📊 游戏历史记录", expanded=False):
            st.write(f"**总游戏场数:** {len(st.session_state.game_history)}")
            if len(st.session_state.game_history) > 0:
                max_score = max(game['score'] for game in st.session_state.game_history)
                avg_score = sum(game['score'] for game in st.session_state.game_history) / len(st.session_state.game_history)
                st.write(f"**最高分:** {max_score:,}")
                st.write(f"**平均分:** {avg_score:.0f}")
                
                st.write("**最近游戏记录:**")
                recent_games = st.session_state.game_history[-5:]
                for game in reversed(recent_games):
                    st.write(f"🕒 {game['timestamp']} - 分数: {game['score']:,} | 等级: {game['level']} | 消行: {game['lines']}")
    
    # 嵌入俄罗斯方块游戏
    components.html(tetris_html, height=750)

# 添加说明信息
st.markdown("---")
st.markdown("""
### 🎯 使用说明：
- **左侧聊天区域**：和AI助手进行对话，询问任何问题
- **右侧游戏区域**：享受经典俄罗斯方块游戏
- **游戏操作**：使用键盘方向键控制方块，空格键快速下降
- **多任务体验**：可以边聊天边游戏，互不干扰！

### 🚀 特色功能：
- 🤖 智能AI对话助手
- 🎮 完整俄罗斯方块游戏
- 📱 响应式设计，适配各种屏幕
- ⚡ 实时游戏体验
""")
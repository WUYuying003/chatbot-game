# 🐦 Voice-Controlled Flying Bird Game

**Part of the Interactive Projects - Mini Games Club**

A real-time voice-controlled flying bird game inspired by the Chrome dinosaur game, built with Python, Pygame, and PyAudio. This innovative game demonstrates advanced human-computer interaction through voice control.

## 🎮 Game Features

### Core Gameplay
- **Voice Control**: Control the bird's vertical position using your voice pitch
- **Real-time Audio Processing**: Advanced FFT-based pitch detection for precise control
- **Obstacle Avoidance**: Navigate through randomly generated pipe obstacles
- **Progressive Difficulty**: Balanced obstacle spacing and speed for optimal challenge
- **Scoring System**: Track your progress with real-time score updates

### Game Controls
- **High Pitch**: Bird flies upward
- **Low Pitch**: Bird flies downward  
- **No Sound**: Bird maintains current position
- **Space Bar**: Pause/Resume game (or restart when game over)
- **ESC Key**: Exit game

### User Interface
- Real-time pitch and volume visualization
- Audio level indicators with visual feedback
- Pause overlay with clear instructions
- Game over screen with final score
- Encouraging score messages

## 📋 Requirements

```
pygame>=2.6.0
numpy>=1.24.0
pyaudio>=0.2.14
```

## 🚀 Installation & Setup

1. **Clone the repository**
```bash
git clone https://github.com/WUYuying003/interactive-projects.git
cd interactive-projects/voice_bird_game
```

2. **Create virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

3. **Install dependencies**
```bash
pip install pygame numpy pyaudio
```

4. **Run the game**
```bash
python voice_bird_game.py
```

## 🎵 Audio Setup

### macOS
```bash
brew install portaudio
pip install pyaudio
```

### Ubuntu/Debian
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

### Windows
PyAudio binaries are usually available via pip. If you encounter issues:
```bash
pip install pipwin
pipwin install pyaudio
```

## 🎯 How to Play

1. **Start the game** - Run `python voice_bird_game.py`
2. **Use your voice** - The game will automatically detect your microphone
3. **Control the bird**:
   - Make high-pitched sounds (whistling, "eee" sounds) to fly up
   - Make low-pitched sounds (humming, "ooo" sounds) to fly down
   - Stay quiet to maintain current height
4. **Avoid obstacles** - Navigate through the green pipe gaps
5. **Score points** - Each obstacle you pass increases your score
6. **Pause anytime** - Press Space to pause/resume
7. **Restart** - When game over, press Space to play again

## 🎮 Game Versions

### voice_bird_game.py (Main Version)
- Advanced pitch detection using FFT analysis
- Precise voice control with frequency mapping
- Professional audio processing
- Full feature set with pause/resume functionality

### simple_voice_bird.py (Simplified Version)
- Volume-based control (easier for beginners)
- Simplified audio processing
- Good for testing audio setup
- Lightweight alternative

## 🔧 Technical Details

### Audio Processing
- **Sample Rate**: 44.1 kHz
- **Pitch Range**: 80-1000 Hz (human voice range)
- **Volume Threshold**: Configurable sensitivity
- **FFT Analysis**: Real-time frequency domain processing

### Game Engine
- **Framework**: Pygame for graphics and input handling
- **Threading**: Separate audio capture thread for smooth performance
- **Collision Detection**: Precise pixel-based collision system
- **Animation**: 60 FPS smooth gameplay

### Difficulty Balancing
- **Obstacle Gap**: 380 pixels (optimized for voice control tolerance)
- **Obstacle Speed**: 2.8 pixels/frame
- **Generation Rate**: Every 2.7 seconds
- **Bird Response**: Smoothed movement with 0.4 responsiveness factor

## 🎤 Microphone Tips

1. **Use a clear microphone** - Built-in laptop mics work, but external mics are better
2. **Minimize background noise** - Play in a quiet environment
3. **Consistent distance** - Keep steady distance from microphone
4. **Practice voice control** - Try different sounds to find what works best
5. **Check audio levels** - Watch the volume bar in-game for feedback

## 🐛 Troubleshooting

### No Audio Input Detected
- Check microphone permissions in system settings
- Verify microphone is working in other applications
- Try running `simple_voice_bird.py` for basic audio testing

### Game Runs Slowly
- Close other audio applications
- Reduce background processes
- Check if audio device supports 44.1 kHz sample rate

### Bird Not Responding to Voice
- Speak louder to meet volume threshold
- Try different pitch ranges (humming vs whistling)
- Check the pitch indicator bar for visual feedback

## 🏆 High Score Tips

1. **Master voice control** - Practice smooth pitch transitions
2. **Stay calm** - Avoid sudden movements that cause crashes
3. **Use the pause feature** - Take breaks to maintain focus
4. **Learn the timing** - Obstacles appear every 2.7 seconds
5. **Find your voice range** - Discover which sounds work best for you

## 🎨 Customization

The game is designed to be easily customizable:
- Modify colors in the color definitions section
- Adjust difficulty by changing obstacle gap size
- Tune audio sensitivity by modifying volume thresholds
- Add new visual effects in the drawing functions

## 📄 License

This project is part of a programming course assignment and is available for educational purposes.

## 🤝 Contributing

Feel free to submit issues and enhancement requests! This project demonstrates:
- Real-time audio processing in Python
- Game development with Pygame
- Multithreaded application design
- Human-computer interaction through voice

---

**Repository**: https://github.com/WUYuying003/interactive-projects  
**Mini Games Club**: Interactive Projects Collection  
**Author**: WUYuying003  
**Contact**: 25056092g@connect.polyu.hk

### 🎮 More Games in Our Club
- AI Chatbot + Tetris Game
- Future gesture-controlled games
- Upcoming multiplayer experiences

**Enjoy playing and happy flying! 🎮🐦**
# 🐦 Voice-Controlled Flying Bird Game - Assignment

**Created by: WUYuying003**  
**Course Assignment: Interactive Programming**  
**Date: October 2025**

## 🎮 Game Demo

![Voice Bird Game Demo](demo.gif)

*Watch the bird respond to voice commands in real-time!*

## 📝 Assignment Overview

This project demonstrates an innovative **voice-controlled flying bird game** that uses real-time audio processing to control gameplay. Players use their voice pitch to navigate a bird through obstacles, showcasing advanced human-computer interaction principles.

### 🎯 Key Learning Objectives Achieved

1. **Real-time Audio Processing**: Implemented FFT-based pitch detection
2. **Game Development**: Created smooth 60fps gameplay with Pygame
3. **Human-Computer Interaction**: Innovative voice control interface
4. **Multithreading**: Separate audio capture thread for performance
5. **Signal Processing**: Audio analysis and frequency domain processing

## 🎵 How It Works

### Voice Control Mechanics
- **High Pitch Sounds** (whistling, "eee"): Bird flies upward
- **Low Pitch Sounds** (humming, "ooo"): Bird flies downward  
- **Silence**: Bird maintains current position
- **Real-time Feedback**: Visual audio indicators show voice input

### Technical Implementation
```python
# Core audio analysis using FFT
def analyze_audio(data):
    audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32)
    volume = np.sqrt(np.mean(audio_data**2))
    
    if volume > 100:
        fft = np.fft.fft(audio_data)
        freqs = np.fft.fftfreq(len(fft), 1/RATE)
        # Find dominant frequency in human voice range (80-1000 Hz)
```

## 🚀 Quick Start Guide

### Prerequisites
```bash
pip install pygame numpy pyaudio
```

### For macOS (Audio Setup)
```bash
brew install portaudio
```

### Run the Game
```bash
python voice_bird_game.py
```

## 🎮 Game Features

### Core Gameplay
- ✅ **Voice-Controlled Movement**: Pitch-based bird control
- ✅ **Obstacle Avoidance**: Navigate through pipe barriers
- ✅ **Progressive Difficulty**: Balanced challenge progression
- ✅ **Real-time Scoring**: Track performance with live updates
- ✅ **Pause/Resume**: Space bar for game control

### Technical Features
- ✅ **Advanced Audio Processing**: 44.1kHz sampling with FFT analysis
- ✅ **Smooth Animation**: 60 FPS rendering with Pygame
- ✅ **Visual Feedback**: Real-time pitch and volume indicators
- ✅ **Error Handling**: Robust audio device management
- ✅ **Cross-platform**: Works on Windows, macOS, and Linux

### User Interface
- ✅ **Intuitive Controls**: Clear voice command instructions
- ✅ **Visual Audio Feedback**: Volume bars and pitch indicators
- ✅ **Game State Management**: Pause overlay and game over screens
- ✅ **Encouraging Feedback**: Positive scoring messages

## 🔧 Technical Architecture

### Audio Processing Pipeline
1. **Capture**: PyAudio streams from microphone (44.1kHz)
2. **Analysis**: NumPy FFT converts to frequency domain
3. **Detection**: Identify dominant frequency in voice range
4. **Mapping**: Convert pitch to bird vertical position
5. **Smoothing**: Apply movement smoothing for natural control

### Game Engine Structure
```
voice_bird_game.py
├── Audio Thread (background)
│   ├── Microphone capture
│   ├── FFT analysis
│   └── Pitch detection
├── Main Game Loop
│   ├── Event handling
│   ├── Game logic updates
│   ├── Collision detection
│   └── Rendering
└── UI Components
    ├── Real-time audio visualization
    ├── Game state displays
    └── Control instructions
```

## 📊 Performance Optimizations

- **Multithreading**: Separate audio capture prevents game lag
- **Buffer Management**: Efficient audio queue handling
- **Collision Detection**: Optimized rectangle-based collision
- **Memory Management**: Proper cleanup of audio resources
- **Frequency Filtering**: Focus on human voice range (80-1000Hz)

## 🎯 Assignment Challenges Solved

### 1. Real-time Audio Processing
**Challenge**: Capturing and analyzing audio without blocking gameplay  
**Solution**: Implemented threaded audio capture with queue-based communication

### 2. Pitch Detection Accuracy
**Challenge**: Reliable pitch detection from noisy microphone input  
**Solution**: FFT-based frequency analysis with noise filtering

### 3. Responsive Game Control
**Challenge**: Smooth bird movement responding to voice changes  
**Solution**: Smoothed target position with configurable responsiveness

### 4. User Experience Design
**Challenge**: Making voice control intuitive and enjoyable  
**Solution**: Visual feedback, clear instructions, and forgiving difficulty

## 🎮 Game Versions Included

### 1. voice_bird_game.py (Main Version)
- **Advanced pitch detection** using FFT analysis
- **Professional audio processing** with noise filtering
- **Complete feature set** with pause/resume functionality
- **Visual audio feedback** with real-time indicators

### 2. simple_voice_bird.py (Educational Version)
- **Volume-based control** for easier understanding
- **Simplified audio processing** for learning
- **Good for testing** audio setup and concepts
- **Lightweight alternative** with core mechanics

## 🎤 Voice Control Tips

### For Best Performance:
1. **Use Clear Sounds**: Whistling (high) and humming (low) work best
2. **Consistent Distance**: Maintain steady distance from microphone
3. **Quiet Environment**: Minimize background noise
4. **Practice Range**: Find your comfortable pitch range
5. **Watch Indicators**: Use visual feedback to optimize control

### Troubleshooting:
- **No response**: Check microphone permissions and volume threshold
- **Lag**: Close other audio applications
- **Inconsistent control**: Try different voice sounds and pitches

## 📚 Educational Value

This project demonstrates several important programming concepts:

### Audio Signal Processing
- Digital signal processing fundamentals
- Fast Fourier Transform (FFT) implementation
- Real-time data streaming and analysis

### Game Development
- Event-driven programming architecture
- Real-time rendering and animation
- User interface design principles

### System Integration
- Hardware-software interaction (microphone)
- Cross-platform compatibility
- Performance optimization techniques

## 🏆 Assignment Achievements

✅ **Innovation**: Created unique voice-controlled gameplay  
✅ **Technical Complexity**: Advanced audio processing implementation  
✅ **User Experience**: Intuitive and engaging interaction design  
✅ **Code Quality**: Clean, documented, and maintainable code  
✅ **Performance**: Smooth 60fps with real-time audio processing  
✅ **Educational**: Demonstrates multiple advanced programming concepts  

## 📁 Project Files

```
voice_controlled_bird_assignment/
├── voice_bird_game.py          # Main game (advanced version)
├── simple_voice_bird.py        # Educational simplified version
├── requirements.txt            # Python dependencies
├── demo.gif                    # Game demonstration video
└── README.md                   # This documentation
```

## 🔗 Dependencies

```txt
pygame>=2.6.0    # Game engine and graphics
numpy>=1.24.0    # Audio signal processing
pyaudio>=0.2.14  # Real-time audio capture
```

## 🎓 Learning Outcomes

Through this project, I have successfully demonstrated:

1. **Advanced Programming Skills**: Complex real-time systems development
2. **Audio Processing Knowledge**: Digital signal processing and FFT analysis  
3. **Game Development Expertise**: Complete game creation with Pygame
4. **UI/UX Design**: Intuitive interface for innovative control method
5. **Performance Optimization**: Multithreaded architecture for smooth gameplay
6. **Problem Solving**: Creative solutions for human-computer interaction

---

## 👨‍🎓 Student Information

**Name**: WUYuying003  
**Email**: 25056092g@connect.polyu.hk  
**Assignment**: Voice-Controlled Interactive Game  
**Course**: Interactive Programming  
**Submission Date**: October 2025  

### 🎯 Project Highlights for Assessment

- **Creativity**: Unique voice control mechanism
- **Technical Depth**: Advanced audio processing and game development
- **Code Quality**: Well-structured, documented, and maintainable
- **User Experience**: Intuitive and engaging gameplay
- **Educational Value**: Demonstrates multiple programming concepts

**Thank you for reviewing my assignment! 🎮🐦**
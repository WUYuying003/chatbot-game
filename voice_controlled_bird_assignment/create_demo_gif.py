"""
Simple GIF recorder for Voice Bird Game Demo
This script helps create a demo GIF of the voice-controlled bird game
"""

import pygame
import sys
import os
from PIL import Image
import time

def create_demo_gif():
    """
    Instructions for creating a demo GIF:
    
    1. Run this script while playing the game
    2. It will capture screenshots for 5 seconds
    3. Screenshots will be converted to GIF
    
    Manual GIF Creation Alternative:
    1. Use screen recording software (QuickTime on macOS, OBS, etc.)
    2. Record 5 seconds of gameplay showing:
       - Bird responding to voice commands
       - Passing through obstacles
       - Real-time audio indicators
    3. Convert to GIF using online tools like:
       - ezgif.com
       - giphy.com
       - convertio.co
    
    GIF Requirements:
    - Duration: 5 seconds
    - Size: Reasonable file size for GitHub (< 10MB)
    - Shows voice control in action
    - Loops seamlessly
    """
    
    print("🎬 GIF Creation Instructions:")
    print("1. Start the voice_bird_game.py")
    print("2. Use screen recording software to record 5 seconds of gameplay")
    print("3. Show bird responding to voice (high/low pitch)")
    print("4. Convert to GIF using online converter")
    print("5. Save as 'demo.gif' in the assignment folder")
    print()
    print("📱 Recommended tools:")
    print("- macOS: QuickTime Player (File > New Screen Recording)")
    print("- Windows: Xbox Game Bar (Win + G)")
    print("- Cross-platform: OBS Studio")
    print()
    print("🌐 GIF Converters:")
    print("- https://ezgif.com/video-to-gif")
    print("- https://giphy.com/create/gifmaker")
    print("- https://convertio.co/mp4-gif/")

if __name__ == "__main__":
    create_demo_gif()
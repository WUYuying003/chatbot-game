import pygame
import numpy as np
import pyaudio
import threading
import queue
import random
import math
import time

# Initialize pygame
pygame.init()

# Game settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
FPS = 60

# Color definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)  # Sky blue
GREEN = (34, 139, 34)   # Forest green
RED = (255, 0, 0)       # Red
YELLOW = (255, 255, 0)  # Yellow
ORANGE = (255, 165, 0)  # Orange

# Audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Audio analysis related variables
audio_queue = queue.Queue()
current_pitch = 0
current_volume = 0

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20
        self.target_y = y
        self.speed = 0.3
        self.color = YELLOW
        
    def update(self, pitch, volume):
        """Update bird position based on pitch and volume"""
        if volume > 80:  # Lower volume threshold from 100 to 80, easier to trigger
            # Adjust target height based on pitch
            # Pitch range is approximately 80-1000 Hz, mapped to screen height
            if pitch > 0:
                # High pitch -> fly high (top of screen)
                # Low pitch -> fly low (bottom of screen)
                normalized_pitch = max(0, min(1, (pitch - 80) / (800 - 80)))
                self.target_y = SCREEN_HEIGHT - 100 - (normalized_pitch * (SCREEN_HEIGHT - 200))
            
            # Smooth movement to target position, increase response speed
            diff = self.target_y - self.y
            self.y += diff * 0.4  # Increase from 0.3 to 0.4, faster response
        
        # Limit within screen boundaries
        self.y = max(self.size, min(SCREEN_HEIGHT - self.size, self.y))
    
    def draw(self, screen):
        """Draw the bird"""
        # Bird body
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        # Bird beak
        beak_points = [
            (self.x + self.size, self.y),
            (self.x + self.size + 15, self.y - 5),
            (self.x + self.size + 15, self.y + 5)
        ]
        pygame.draw.polygon(screen, ORANGE, beak_points)
        # Bird eye
        pygame.draw.circle(screen, BLACK, (int(self.x + 8), int(self.y - 5)), 3)

class Obstacle:
    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(200, SCREEN_HEIGHT - 200)  # Increase margins
        self.gap_size = 380  # Increased from 320 to 380, larger gap for easier passage
        self.width = 60
        self.speed = 2.8  # Increased from 2.2 to 2.8, slightly faster
        self.color = GREEN
        self.passed = False
        
    def update(self):
        """Update obstacle position"""
        self.x -= self.speed
        
    def draw(self, screen):
        """Draw obstacles (pipes)"""
        # Upper pipe
        pygame.draw.rect(screen, self.color, 
                        (self.x, 0, self.width, self.gap_y - self.gap_size//2))
        # Lower pipe
        pygame.draw.rect(screen, self.color,
                        (self.x, self.gap_y + self.gap_size//2, self.width, 
                         SCREEN_HEIGHT - (self.gap_y + self.gap_size//2)))
        
        # Pipe edges
        pygame.draw.rect(screen, BLACK, 
                        (self.x, 0, self.width, self.gap_y - self.gap_size//2), 3)
        pygame.draw.rect(screen, BLACK,
                        (self.x, self.gap_y + self.gap_size//2, self.width, 
                         SCREEN_HEIGHT - (self.gap_y + self.gap_size//2)), 3)
    
    def collides_with_bird(self, bird):
        """Detect collision with bird"""
        if (bird.x + bird.size > self.x and bird.x - bird.size < self.x + self.width):
            if (bird.y - bird.size < self.gap_y - self.gap_size//2 or 
                bird.y + bird.size > self.gap_y + self.gap_size//2):
                return True
        return False
    
    def is_off_screen(self):
        """Check if obstacle is off screen"""
        return self.x + self.width < 0

def analyze_audio(data):
    """Analyze audio data to extract pitch and volume"""
    # Convert to numpy array
    audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32)
    
    # Calculate volume (RMS)
    volume = np.sqrt(np.mean(audio_data**2))
    
    # Simple pitch detection (based on zero-crossing rate and spectral analysis)
    pitch = 0
    if volume > 100:  # Only analyze pitch when there's sufficient volume
        # Use FFT for spectral analysis
        fft = np.fft.fft(audio_data)
        freqs = np.fft.fftfreq(len(fft), 1/RATE)
        
        # Only look at positive frequencies
        magnitude = np.abs(fft[:len(fft)//2])
        freqs = freqs[:len(freqs)//2]
        
        # Find dominant frequency (exclude low-frequency noise)
        valid_range = (freqs > 80) & (freqs < 1000)  # Human voice range
        if np.any(valid_range):
            valid_magnitude = magnitude[valid_range]
            valid_freqs = freqs[valid_range]
            if len(valid_magnitude) > 0 and np.max(valid_magnitude) > 0:
                pitch = valid_freqs[np.argmax(valid_magnitude)]
    
    return pitch, volume

def audio_callback():
    """Audio capture thread"""
    p = pyaudio.PyAudio()
    
    try:
        default_input = p.get_default_input_device_info()
        print(f"🎤 Using audio device: {default_input['name']}")
        
        stream = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       input=True,
                       input_device_index=default_input['index'],
                       frames_per_buffer=CHUNK)
        
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            pitch, volume = analyze_audio(data)
            audio_queue.put((pitch, volume))
            
    except Exception as e:
        print(f"Audio error: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

def draw_ui(screen, score, pitch, volume, game_over=False, paused=False):
    """Draw user interface"""
    font = pygame.font.Font(None, 48)  # Increase font size
    small_font = pygame.font.Font(None, 28)
    
    # Score - more prominent display
    score_text = font.render(f"🏆 Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    # Audio information
    pitch_text = small_font.render(f"Pitch: {pitch:.1f} Hz", True, BLACK)
    volume_text = small_font.render(f"Volume: {volume:.1f}", True, BLACK)
    screen.blit(pitch_text, (10, 70))
    screen.blit(volume_text, (10, 95))
    
    # Volume bar
    bar_width = 200
    bar_height = 12
    volume_ratio = min(1.0, volume / 1000)
    pygame.draw.rect(screen, BLACK, (10, 120, bar_width, bar_height), 2)
    pygame.draw.rect(screen, GREEN, (10, 120, int(bar_width * volume_ratio), bar_height))
    
    # Pitch indicator
    pitch_indicator_y = 140
    if pitch > 0:
        normalized_pitch = max(0, min(1, (pitch - 80) / (800 - 80)))
        indicator_x = 10 + int(bar_width * normalized_pitch)
        pygame.draw.circle(screen, RED, (indicator_x, pitch_indicator_y + 15), 6)
    
    pygame.draw.rect(screen, BLACK, (10, pitch_indicator_y, bar_width, 30), 2)
    pitch_label = small_font.render("Pitch Level", True, BLACK)
    screen.blit(pitch_label, (10, pitch_indicator_y - 25))
    
    # Control instructions
    if paused:
        instructions = [
            "⏸️ GAME PAUSED",
            "• Press SPACE to continue",
            "• Press ESC to quit"
        ]
        for i, instruction in enumerate(instructions):
            inst_text = small_font.render(instruction, True, BLACK)
            screen.blit(inst_text, (10, 190 + i * 28))
    else:
        instructions = [
            "🎤 Voice Controls:",
            "• High pitch = Fly high",
            "• Low pitch = Fly low", 
            "• No sound = Stay still",
            "• Press SPACE to pause",
            "• Avoid green obstacles!"
        ]
        for i, instruction in enumerate(instructions):
            inst_text = small_font.render(instruction, True, BLACK)
            screen.blit(inst_text, (10, 190 + i * 28))
    
    if paused:
        # Pause state overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(64)  # Slight transparency
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        big_font = pygame.font.Font(None, 96)
        pause_text = big_font.render("⏸️ PAUSED", True, WHITE)
        continue_text = font.render("Press SPACE to continue", True, WHITE)
        
        # Center display
        screen.blit(pause_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 50))
        screen.blit(continue_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 20))
    
    if game_over:
        # Game over interface - larger and more prominent
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)  # Semi-transparent
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        big_font = pygame.font.Font(None, 72)
        medium_font = pygame.font.Font(None, 36)
        
        game_over_text = big_font.render("💀 GAME OVER!", True, RED)
        final_score_text = medium_font.render(f"🏆 Final Score: {score} obstacles passed!", True, WHITE)
        restart_text = medium_font.render("⌨️ Press SPACE to restart", True, WHITE)
        quit_text = small_font.render("Press ESC to quit", True, WHITE)
        
        # Center display
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - 180, SCREEN_HEIGHT//2 - 100))
        screen.blit(final_score_text, (SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 40))
        screen.blit(restart_text, (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 + 20))
        screen.blit(quit_text, (SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 + 60))

def main():
    """Main game loop"""
    global current_pitch, current_volume
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("🐦 Voice-Controlled Flying Bird Game")
    clock = pygame.time.Clock()
    
    # Start audio thread
    audio_thread = threading.Thread(target=audio_callback, daemon=True)
    audio_thread.start()
    
    print("🎮 Game started!")
    print("🎤 Use your voice to control the bird:")
    print("   High pitch = fly high, Low pitch = fly low")
    print("   No sound = stay still")
    print("🎯 Avoid the green obstacles!")
    
    while True:
        # Initialize game objects
        bird = Bird(150, SCREEN_HEIGHT // 2)
        obstacles = []
        score = 0
        game_over = False
        paused = False  # Add pause state
        obstacle_timer = 0
        
        print("🎮 New game started!")
        
        # Main game loop
        running = True
        while running:
            dt = clock.tick(FPS)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
                    elif event.key == pygame.K_SPACE:
                        if game_over:
                            # Restart when game is over
                            print("🔄 Restarting game...")
                            running = False
                            break
                        else:
                            # Pause/resume during gameplay
                            paused = not paused
                            if paused:
                                print("⏸️ Game paused - Press SPACE to continue")
                            else:
                                print("▶️ Game resumed")
            
            if game_over:
                # Game over state, only draw UI
                screen.fill(BLUE)
                draw_ui(screen, score, current_pitch, current_volume, game_over=True, paused=False)
                pygame.display.flip()
                continue
            
            if paused:
                # Paused state, only draw UI, don't update game logic
                screen.fill(BLUE)
                # Draw clouds (decoration)
                for i in range(5):
                    cloud_x = (i * 300 + pygame.time.get_ticks() * 0.02) % (SCREEN_WIDTH + 100)
                    cloud_y = 50 + i * 30
                    pygame.draw.circle(screen, WHITE, (int(cloud_x), cloud_y), 25)
                    pygame.draw.circle(screen, WHITE, (int(cloud_x + 20), cloud_y), 30)
                    pygame.draw.circle(screen, WHITE, (int(cloud_x + 40), cloud_y), 25)
                
                # Draw obstacles
                for obstacle in obstacles:
                    obstacle.draw(screen)
                
                # Draw bird
                bird.draw(screen)
                
                # Draw UI
                draw_ui(screen, score, current_pitch, current_volume, game_over=False, paused=True)
                pygame.display.flip()
                continue
            
            # Get audio data
            while not audio_queue.empty():
                current_pitch, current_volume = audio_queue.get()
            
            # Update bird
            bird.update(current_pitch, current_volume)
            
            # Generate new obstacles
            obstacle_timer += dt
            if obstacle_timer > 2700:  # Reduced from 3 seconds to 2.7 seconds, slightly faster
                obstacles.append(Obstacle(SCREEN_WIDTH))
                obstacle_timer = 0
            
            # Update obstacles
            for obstacle in obstacles[:]:
                obstacle.update()
                
                # Detect collision
                if obstacle.collides_with_bird(bird):
                    game_over = True
                    print(f"💀 Game Over! Final Score: {score}")
                
                # Detect passing obstacles
                if not obstacle.passed and obstacle.x + obstacle.width < bird.x:
                    obstacle.passed = True
                    score += 1
                    print(f"🎉 Great! Score: {score} obstacles passed!")  # More encouraging message
                
                # Remove off-screen obstacles
                if obstacle.is_off_screen():
                    obstacles.remove(obstacle)
            
            # Draw game
            screen.fill(BLUE)  # Sky background
            
            # Draw clouds (decoration)
            for i in range(5):
                cloud_x = (i * 300 + pygame.time.get_ticks() * 0.02) % (SCREEN_WIDTH + 100)
                cloud_y = 50 + i * 30
                pygame.draw.circle(screen, WHITE, (int(cloud_x), cloud_y), 25)
                pygame.draw.circle(screen, WHITE, (int(cloud_x + 20), cloud_y), 30)
                pygame.draw.circle(screen, WHITE, (int(cloud_x + 40), cloud_y), 25)
            
            # Draw obstacles
            for obstacle in obstacles:
                obstacle.draw(screen)
            
            # Draw bird
            bird.draw(screen)
            
            # Draw UI
            draw_ui(screen, score, current_pitch, current_volume, game_over=False, paused=False)
            
            pygame.display.flip()

if __name__ == "__main__":
    main()
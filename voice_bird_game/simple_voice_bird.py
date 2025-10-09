import pygame
import numpy as np
import pyaudio
import threading
import queue
import random
import sys

# 简化版声控飞鸟游戏

pygame.init()

# 游戏设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 150, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# 音频设置
audio_queue = queue.Queue()
current_volume = 0

class SimpleBird:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.size = 15
        self.dy = 0  # 垂直速度
        
    def update(self, volume):
        # 根据音量控制飞行，降低阈值让控制更容易
        if volume > 150:  # 从200降低到150，更容易触发
            self.dy = -2.5  # 稍微降低上升速度，从-3到-2.5
        else:  # 无声音时下降
            self.dy = 1.5   # 稍微降低下降速度，从2到1.5
            
        self.y += self.dy
        
        # 限制在屏幕内
        if self.y < self.size:
            self.y = self.size
        if self.y > SCREEN_HEIGHT - self.size:
            self.y = SCREEN_HEIGHT - self.size
    
    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (self.x, int(self.y)), self.size)
        # 简单的眼睛
        pygame.draw.circle(screen, BLACK, (self.x + 5, int(self.y - 3)), 2)

class SimpleObstacle:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.gap_center = random.randint(180, SCREEN_HEIGHT - 180)  # 增加边距
        self.gap_size = 250  # 从220增加到250，缝隙更大
        self.width = 50
        self.speed = 2.6  # 从2.2提高到2.6，稍微快一点
        
    def update(self):
        self.x -= self.speed
        
    def draw(self, screen):
        # 上方障碍
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.gap_center - self.gap_size//2))
        # 下方障碍  
        pygame.draw.rect(screen, GREEN, (self.x, self.gap_center + self.gap_size//2, self.width, SCREEN_HEIGHT))
    
    def hits_bird(self, bird):
        if bird.x + bird.size > self.x and bird.x - bird.size < self.x + self.width:
            if bird.y < self.gap_center - self.gap_size//2 or bird.y > self.gap_center + self.gap_size//2:
                return True
        return False
    
    def is_passed(self, bird):
        return self.x + self.width < bird.x
    
    def is_off_screen(self):
        return self.x + self.width < 0

def audio_thread():
    """简化的音频处理"""
    global current_volume
    
    p = pyaudio.PyAudio()
    
    try:
        # 获取默认输入设备
        default_input = p.get_default_input_device_info()
        print(f"🎤 Using audio device: {default_input['name']}")
        
        stream = p.open(format=pyaudio.paInt16,
                       channels=1,
                       rate=44100,
                       input=True,
                       input_device_index=default_input['index'],
                       frames_per_buffer=1024)
        
        print("🎤 Audio capture started...")
        
        while True:
            try:
                data = stream.read(1024, exception_on_overflow=False)
                audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32)
                
                # 安全的音量计算，避免NaN
                if len(audio_data) > 0:
                    mean_square = np.mean(audio_data**2)
                    if mean_square >= 0:  # 确保非负数
                        volume = np.sqrt(mean_square)
                        if not np.isnan(volume) and not np.isinf(volume):
                            current_volume = volume
                        else:
                            current_volume = 0
                    else:
                        current_volume = 0
                else:
                    current_volume = 0
                    
            except Exception as e:
                print(f"Audio processing error: {e}")
                current_volume = 0
                
    except Exception as e:
        print(f"Audio setup error: {e}")
    finally:
        try:
            stream.stop_stream()
            stream.close()
        except:
            pass
        p.terminate()

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("🐦 Simple Voice Bird")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    # 启动音频线程
    audio_thread_obj = threading.Thread(target=audio_thread, daemon=True)
    audio_thread_obj.start()
    
    print("🎮 Simple Voice Bird Game")
    print("🎤 Make sound to fly up, stay quiet to fall down")
    print("🎯 Avoid green obstacles!")
    
    bird = SimpleBird()
    obstacles = []
    score = 0
    game_over = False
    spawn_timer = 0
    
    running = True
    while running:
        dt = clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_over:
                    # 重新开始
                    print("🔄 Restarting game...")
                    bird = SimpleBird()
                    obstacles = []
                    score = 0
                    game_over = False
                    spawn_timer = 0
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        if not game_over:
            # 更新游戏
            bird.update(current_volume)
            
            # 生成障碍物
            spawn_timer += dt
            if spawn_timer > 2900:  # 从3.2秒减少到2.9秒，稍微快一点
                obstacles.append(SimpleObstacle())
                spawn_timer = 0
            
            # 更新障碍物
            for obs in obstacles[:]:
                obs.update()
                
                if obs.hits_bird(bird):
                    game_over = True
                    print(f"💀 Game Over! Score: {score}")
                
                if obs.is_passed(bird) and not hasattr(obs, 'scored'):
                    score += 1
                    obs.scored = True
                    print(f"🎉 Awesome! {score} obstacles passed!")  # 更鼓励的信息
                
                if obs.is_off_screen():
                    obstacles.remove(obs)
        
        # 绘制
        screen.fill(BLUE)
        
        # 绘制障碍物
        for obs in obstacles:
            obs.draw(screen)
        
        # 绘制小鸟
        bird.draw(screen)
        
        # UI
        big_font = pygame.font.Font(None, 48)
        score_text = big_font.render(f"🏆 Score: {score}", True, WHITE)
        volume_text = font.render(f"Volume: {int(current_volume)}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(volume_text, (10, 60))
        
        # 音量条
        volume_bar_width = min(200, current_volume / 2)
        pygame.draw.rect(screen, WHITE, (10, 100, volume_bar_width, 12))
        
        # 控制提示
        if current_volume > 150:  # 更新阈值显示
            status_text = font.render("🔊 FLYING UP!", True, WHITE)
        else:
            status_text = font.render("🔇 falling down...", True, WHITE)
        screen.blit(status_text, (10, 130))
        
        if game_over:
            # 半透明覆盖层
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            big_font = pygame.font.Font(None, 64)
            game_over_text = big_font.render("💀 GAME OVER!", True, RED)
            final_score_text = font.render(f"🏆 You passed {score} obstacles!", True, WHITE)
            restart_text = font.render("⌨️ Press SPACE to restart", True, WHITE)
            
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - 160, SCREEN_HEIGHT//2 - 80))
            screen.blit(final_score_text, (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 - 20))
            screen.blit(restart_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 20))
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
import pygame
import random
import sys

# 初始化Pygame
pygame.init()

# 游戏常量
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30
GRID_X_OFFSET = 50
GRID_Y_OFFSET = 50

# 计算窗口大小
WINDOW_WIDTH = GRID_WIDTH * BLOCK_SIZE + GRID_X_OFFSET * 2 + 200  # 额外空间显示信息
WINDOW_HEIGHT = GRID_HEIGHT * BLOCK_SIZE + GRID_Y_OFFSET * 2

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)

# 俄罗斯方块形状定义
SHAPES = [
    # I形状
    [
        ['.....',
         '..#..',
         '..#..',
         '..#..',
         '..#..'],
        ['.....',
         '.....',
         '####.',
         '.....',
         '.....']
    ],
    # O形状
    [
        ['.....',
         '.....',
         '.##..',
         '.##..',
         '.....']
    ],
    # T形状
    [
        ['.....',
         '.....',
         '.#...',
         '###..',
         '.....'],
        ['.....',
         '.....',
         '.#...',
         '.##..',
         '.#...'],
        ['.....',
         '.....',
         '.....',
         '###..',
         '.#...'],
        ['.....',
         '.....',
         '.#...',
         '##...',
         '.#...']
    ],
    # S形状
    [
        ['.....',
         '.....',
         '.##..',
         '##...',
         '.....'],
        ['.....',
         '.#...',
         '.##..',
         '..#..',
         '.....']
    ],
    # Z形状
    [
        ['.....',
         '.....',
         '##...',
         '.##..',
         '.....'],
        ['.....',
         '..#..',
         '.##..',
         '.#...',
         '.....']
    ],
    # J形状
    [
        ['.....',
         '.#...',
         '.#...',
         '##...',
         '.....'],
        ['.....',
         '.....',
         '#....',
         '###..',
         '.....'],
        ['.....',
         '.##..',
         '.#...',
         '.#...',
         '.....'],
        ['.....',
         '.....',
         '###..',
         '..#..',
         '.....']
    ],
    # L形状
    [
        ['.....',
         '..#..',
         '..#..',
         '.##..',
         '.....'],
        ['.....',
         '.....',
         '###..',
         '#....',
         '.....'],
        ['.....',
         '##...',
         '.#...',
         '.#...',
         '.....'],
        ['.....',
         '.....',
         '..#..',
         '###..',
         '.....']
    ]
]

# 形状颜色
SHAPE_COLORS = [CYAN, YELLOW, PURPLE, GREEN, RED, BLUE, ORANGE]

class Piece:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = random.choice(SHAPES)
        self.color = random.choice(SHAPE_COLORS)
        self.rotation = 0
        
    def get_rotated_shape(self):
        return self.shape[self.rotation % len(self.shape)]

class Tetris:
    def __init__(self):
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.get_new_piece()
        self.next_piece = self.get_new_piece()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_time = 0
        self.fall_speed = 500  # 毫秒
        
    def get_new_piece(self):
        return Piece(GRID_WIDTH // 2 - 2, 0)
    
    def valid_move(self, piece, dx, dy, rotation=None):
        if rotation is None:
            rotation = piece.rotation
            
        shape = piece.shape[rotation % len(piece.shape)]
        
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell == '#':
                    x = piece.x + j + dx
                    y = piece.y + i + dy
                    
                    if (x < 0 or x >= GRID_WIDTH or 
                        y >= GRID_HEIGHT or 
                        (y >= 0 and self.grid[y][x] != BLACK)):
                        return False
        return True
    
    def place_piece(self, piece):
        shape = piece.get_rotated_shape()
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell == '#':
                    x = piece.x + j
                    y = piece.y + i
                    if y >= 0:
                        self.grid[y][x] = piece.color
    
    def clear_lines(self):
        lines_to_clear = []
        for y in range(GRID_HEIGHT):
            if all(cell != BLACK for cell in self.grid[y]):
                lines_to_clear.append(y)
        
        for y in lines_to_clear:
            del self.grid[y]
            self.grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])
        
        lines_cleared = len(lines_to_clear)
        self.lines_cleared += lines_cleared
        self.score += lines_cleared * 100 * self.level
        self.level = self.lines_cleared // 10 + 1
        self.fall_speed = max(50, 500 - (self.level - 1) * 50)
        
        return lines_cleared > 0
    
    def game_over(self):
        return not self.valid_move(self.current_piece, 0, 0)
    
    def update(self, dt):
        self.fall_time += dt
        if self.fall_time >= self.fall_speed:
            if self.valid_move(self.current_piece, 0, 1):
                self.current_piece.y += 1
            else:
                self.place_piece(self.current_piece)
                self.clear_lines()
                self.current_piece = self.next_piece
                self.next_piece = self.get_new_piece()
            self.fall_time = 0
    
    def move_piece(self, dx):
        if self.valid_move(self.current_piece, dx, 0):
            self.current_piece.x += dx
    
    def rotate_piece(self):
        new_rotation = (self.current_piece.rotation + 1) % len(self.current_piece.shape)
        if self.valid_move(self.current_piece, 0, 0, new_rotation):
            self.current_piece.rotation = new_rotation
    
    def drop_piece(self):
        while self.valid_move(self.current_piece, 0, 1):
            self.current_piece.y += 1
            self.score += 2

def draw_grid(screen, tetris):
    # 绘制游戏网格背景
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(
                GRID_X_OFFSET + x * BLOCK_SIZE,
                GRID_Y_OFFSET + y * BLOCK_SIZE,
                BLOCK_SIZE,
                BLOCK_SIZE
            )
            pygame.draw.rect(screen, tetris.grid[y][x], rect)
            pygame.draw.rect(screen, WHITE, rect, 1)

def draw_piece(screen, piece):
    shape = piece.get_rotated_shape()
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell == '#':
                x = piece.x + j
                y = piece.y + i
                if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                    rect = pygame.Rect(
                        GRID_X_OFFSET + x * BLOCK_SIZE,
                        GRID_Y_OFFSET + y * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE
                    )
                    pygame.draw.rect(screen, piece.color, rect)
                    pygame.draw.rect(screen, WHITE, rect, 1)

def draw_next_piece(screen, piece, font):
    # 绘制下一个方块
    text = font.render("下一个:", True, WHITE)
    screen.blit(text, (GRID_X_OFFSET + GRID_WIDTH * BLOCK_SIZE + 20, 100))
    
    shape = piece.get_rotated_shape()
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell == '#':
                rect = pygame.Rect(
                    GRID_X_OFFSET + GRID_WIDTH * BLOCK_SIZE + 20 + j * 20,
                    130 + i * 20,
                    20,
                    20
                )
                pygame.draw.rect(screen, piece.color, rect)
                pygame.draw.rect(screen, WHITE, rect, 1)

def draw_info(screen, tetris, font):
    # 绘制游戏信息
    score_text = font.render(f"分数: {tetris.score}", True, WHITE)
    level_text = font.render(f"等级: {tetris.level}", True, WHITE)
    lines_text = font.render(f"行数: {tetris.lines_cleared}", True, WHITE)
    
    screen.blit(score_text, (GRID_X_OFFSET + GRID_WIDTH * BLOCK_SIZE + 20, 20))
    screen.blit(level_text, (GRID_X_OFFSET + GRID_WIDTH * BLOCK_SIZE + 20, 50))
    screen.blit(lines_text, (GRID_X_OFFSET + GRID_WIDTH * BLOCK_SIZE + 20, 80))
    
    # 控制说明
    controls = [
        "控制说明:",
        "←→ 移动",
        "↑ 旋转", 
        "↓ 软降",
        "空格 硬降",
        "R 重新开始",
        "ESC 退出"
    ]
    
    for i, text in enumerate(controls):
        color = YELLOW if i == 0 else WHITE
        control_text = font.render(text, True, color)
        screen.blit(control_text, (GRID_X_OFFSET + GRID_WIDTH * BLOCK_SIZE + 20, 250 + i * 25))

def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("俄罗斯方块")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    big_font = pygame.font.Font(None, 48)
    
    tetris = Tetris()
    running = True
    game_over = False
    
    while running:
        dt = clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    tetris = Tetris()
                    game_over = False
                elif not game_over:
                    if event.key == pygame.K_LEFT:
                        tetris.move_piece(-1)
                    elif event.key == pygame.K_RIGHT:
                        tetris.move_piece(1)
                    elif event.key == pygame.K_DOWN:
                        if tetris.valid_move(tetris.current_piece, 0, 1):
                            tetris.current_piece.y += 1
                            tetris.score += 1
                    elif event.key == pygame.K_UP:
                        tetris.rotate_piece()
                    elif event.key == pygame.K_SPACE:
                        tetris.drop_piece()
        
        if not game_over:
            tetris.update(dt)
            if tetris.game_over():
                game_over = True
        
        # 绘制
        screen.fill(BLACK)
        draw_grid(screen, tetris)
        
        if not game_over:
            draw_piece(screen, tetris.current_piece)
        
        draw_next_piece(screen, tetris.next_piece, font)
        draw_info(screen, tetris, font)
        
        if game_over:
            game_over_text = big_font.render("游戏结束!", True, RED)
            restart_text = font.render("按 R 重新开始", True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
            screen.blit(game_over_text, text_rect)
            screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
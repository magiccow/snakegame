import pygame
import random
import math
import sys

class SnakeGame:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.DARK_GREEN = (0, 150, 0)
        self.BROWN = (139, 69, 19)
        self.LIGHT_BROWN = (160, 82, 45)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.PINK = (255, 192, 203)
        
        # Game settings
        self.cell_size = 20
        self.game_speed = 10
        
        # Initialize game state
        self.reset_game()
    
    def reset_game(self):
        """Reset the game to initial state"""
        # Snake starts in the middle, moving right
        start_x = self.width // 2
        start_y = self.height // 2
        self.snake = [
            [start_x, start_y],
            [start_x - self.cell_size, start_y],
            [start_x - 2 * self.cell_size, start_y]
        ]
        self.direction = [self.cell_size, 0]  # Moving right
        self.score = 0
        self.game_over = False
        self.spawn_mouse()
    
    def spawn_mouse(self):
        """Spawn a new mouse at random location"""
        while True:
            x = random.randint(0, (self.width - self.cell_size) // self.cell_size) * self.cell_size
            y = random.randint(0, (self.height - self.cell_size) // self.cell_size) * self.cell_size
            if [x, y] not in self.snake:
                self.mouse_pos = [x, y]
                break
    
    def draw_mouse(self):
        """Draw a brown mouse with ears and tail"""
        x, y = self.mouse_pos
        
        # Mouse body (brown circle)
        pygame.draw.circle(self.screen, self.BROWN, 
                         (x + self.cell_size // 2, y + self.cell_size // 2), 
                         self.cell_size // 2 - 2)
        
        # Mouse ears (small brown circles)
        ear_size = 4
        pygame.draw.circle(self.screen, self.LIGHT_BROWN,
                         (x + 6, y + 4), ear_size)
        pygame.draw.circle(self.screen, self.LIGHT_BROWN,
                         (x + 14, y + 4), ear_size)
        
        # Mouse eyes (small black dots)
        pygame.draw.circle(self.screen, self.BLACK,
                         (x + 8, y + 8), 2)
        pygame.draw.circle(self.screen, self.BLACK,
                         (x + 12, y + 8), 2)
        
        # Mouse nose (pink dot)
        pygame.draw.circle(self.screen, self.PINK,
                         (x + 10, y + 12), 1)
        
        # Mouse tail (thin brown line)
        tail_start = (x + self.cell_size - 2, y + self.cell_size // 2)
        tail_end = (x + self.cell_size + 8, y + self.cell_size // 2 + 3)
        pygame.draw.line(self.screen, self.BROWN, tail_start, tail_end, 2)
    
    def draw_snake(self):
        """Draw snake with detailed head and tapered tail"""
        if not self.snake:
            return
        
        # Draw snake body segments (getting smaller towards tail)
        for i, segment in enumerate(self.snake):
            x, y = segment
            
            if i == 0:  # Head
                self.draw_snake_head(x, y)
            else:  # Body segments with tapering
                # Calculate segment size (tapers towards tail)
                size_factor = max(0.3, 1.0 - (i - 1) * 0.1)
                segment_size = int(self.cell_size * size_factor)
                offset = (self.cell_size - segment_size) // 2
                
                # Alternate colors for body pattern
                color = self.DARK_GREEN if i % 2 == 0 else self.GREEN
                pygame.draw.rect(self.screen, color,
                               (x + offset, y + offset, segment_size, segment_size))
                
                # Add scales pattern
                if segment_size > 8:
                    scale_color = self.GREEN if i % 2 == 0 else self.DARK_GREEN
                    pygame.draw.rect(self.screen, scale_color,
                                   (x + offset + 2, y + offset + 2, 
                                    segment_size - 4, segment_size - 4))
    
    def draw_snake_head(self, x, y):
        """Draw detailed snake head with eyes and direction"""
        # Head base (green rectangle)
        pygame.draw.rect(self.screen, self.GREEN, (x, y, self.cell_size, self.cell_size))
        
        # Determine head direction for eye placement
        dx, dy = self.direction
        
        # Snake eyes (red dots)
        if dx > 0:  # Moving right
            eye1_pos = (x + 15, y + 5)
            eye2_pos = (x + 15, y + 15)
        elif dx < 0:  # Moving left
            eye1_pos = (x + 5, y + 5)
            eye2_pos = (x + 5, y + 15)
        elif dy > 0:  # Moving down
            eye1_pos = (x + 5, y + 15)
            eye2_pos = (x + 15, y + 15)
        else:  # Moving up
            eye1_pos = (x + 5, y + 5)
            eye2_pos = (x + 15, y + 5)
        
        pygame.draw.circle(self.screen, self.RED, eye1_pos, 2)
        pygame.draw.circle(self.screen, self.RED, eye2_pos, 2)
        
        # Snake tongue (small red line extending from head)
        if dx > 0:  # Moving right
            tongue_start = (x + self.cell_size, y + self.cell_size // 2)
            tongue_end = (x + self.cell_size + 6, y + self.cell_size // 2)
        elif dx < 0:  # Moving left
            tongue_start = (x, y + self.cell_size // 2)
            tongue_end = (x - 6, y + self.cell_size // 2)
        elif dy > 0:  # Moving down
            tongue_start = (x + self.cell_size // 2, y + self.cell_size)
            tongue_end = (x + self.cell_size // 2, y + self.cell_size + 6)
        else:  # Moving up
            tongue_start = (x + self.cell_size // 2, y)
            tongue_end = (x + self.cell_size // 2, y - 6)
        
        pygame.draw.line(self.screen, self.RED, tongue_start, tongue_end, 2)
    
    def handle_input(self):
        """Handle keyboard input for snake direction"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != [0, self.cell_size]:
                    self.direction = [0, -self.cell_size]
                elif event.key == pygame.K_DOWN and self.direction != [0, -self.cell_size]:
                    self.direction = [0, self.cell_size]
                elif event.key == pygame.K_LEFT and self.direction != [self.cell_size, 0]:
                    self.direction = [-self.cell_size, 0]
                elif event.key == pygame.K_RIGHT and self.direction != [-self.cell_size, 0]:
                    self.direction = [self.cell_size, 0]
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
        return True
    
    def update_snake(self):
        """Update snake position and check collisions"""
        if self.game_over:
            return
        
        # Move snake head
        head = self.snake[0].copy()
        head[0] += self.direction[0]
        head[1] += self.direction[1]
        
        # Check wall collision
        if (head[0] < 0 or head[0] >= self.width or 
            head[1] < 0 or head[1] >= self.height):
            self.game_over = True
            return
        
        # Check self collision
        if head in self.snake:
            self.game_over = True
            return
        
        # Add new head
        self.snake.insert(0, head)
        
        # Check if mouse is eaten
        if head == self.mouse_pos:
            self.score += 1
            self.spawn_mouse()
            # Increase speed slightly
            self.game_speed = min(20, self.game_speed + 0.5)
        else:
            # Remove tail if no food eaten
            self.snake.pop()
    
    def draw_ui(self):
        """Draw score and game over screen"""
        font = pygame.font.Font(None, 36)
        
        # Draw score
        score_text = font.render(f"Score: {self.score}", True, self.WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw game over screen
        if self.game_over:
            game_over_text = font.render("GAME OVER", True, self.RED)
            restart_text = font.render("Press R to restart", True, self.WHITE)
            
            # Center the text
            game_over_rect = game_over_text.get_rect(center=(self.width//2, self.height//2))
            restart_rect = restart_text.get_rect(center=(self.width//2, self.height//2 + 50))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(restart_text, restart_rect)
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            running = self.handle_input()
            
            if not self.game_over:
                self.update_snake()
            
            # Draw everything
            self.screen.fill(self.BLACK)
            self.draw_mouse()
            self.draw_snake()
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(self.game_speed)
        
        pygame.quit()
        sys.exit()

# Run the game
if __name__ == "__main__":
    game = SnakeGame()
    game.run()

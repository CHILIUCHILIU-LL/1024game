#!/usr/bin/env python3
"""
1024 Game - Pygame Graphical Version
A beautiful graphical version with animations and particle effects
"""

import sys
import os
import math
import random

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame
from pygame import mixer
from game import Game

# Initialize Pygame
pygame.init()
mixer.init()

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 750
GRID_SIZE = 4
CELL_SIZE = 120
CELL_PADDING = 15
GRID_OFFSET_X = 60
GRID_OFFSET_Y = 180

# Colors
BACKGROUND_COLOR = (250, 248, 239)
GRID_BACKGROUND = (187, 173, 160)
CELL_EMPTY = (205, 193, 180)

# Tile colors for different values
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

# Text colors
TEXT_DARK = (119, 110, 101)
TEXT_LIGHT = (255, 255, 255)
TEXT_COLORS = {
    2: TEXT_DARK,
    4: TEXT_DARK,
    8: TEXT_LIGHT,
    16: TEXT_LIGHT,
    32: TEXT_LIGHT,
    64: TEXT_LIGHT,
    128: TEXT_LIGHT,
    256: TEXT_LIGHT,
    512: TEXT_LIGHT,
    1024: TEXT_LIGHT,
    2048: TEXT_LIGHT,
}


class Particle:
    """Particle effect for animations"""
    def __init__(self, x, y, color, velocity=None, size=None, lifetime=None):
        self.x = x
        self.y = y
        self.color = color
        self.vx = velocity[0] if velocity else random.uniform(-3, 3)
        self.vy = velocity[1] if velocity else random.uniform(-5, -2)
        self.size = size if size else random.randint(4, 10)
        self.lifetime = lifetime if lifetime else random.randint(30, 60)
        self.max_lifetime = self.lifetime
        self.gravity = 0.15
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.lifetime -= 1
        # Fade out
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        return alpha > 0
    
    def draw(self, screen):
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        color_with_alpha = (*self.color[:3], alpha)
        # Create a surface with per-pixel alpha
        particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(particle_surface, color_with_alpha, (self.size, self.size), self.size)
        screen.blit(particle_surface, (int(self.x - self.size), int(self.y - self.size)))


class AnimatedTile:
    """Tile with animation support"""
    def __init__(self, value, row, col, is_new=False):
        self.value = value
        self.row = row
        self.col = col
        self.target_row = row
        self.target_col = col
        self.is_new = is_new
        self.is_merging = False
        
        # Animation properties
        self.scale = 0.1 if is_new else 1.0
        self.target_scale = 1.0
        self.merge_scale = 1.0
        self.opacity = 255
        
        # Position (for smooth movement)
        self.x = GRID_OFFSET_X + col * (CELL_SIZE + CELL_PADDING) + CELL_PADDING
        self.y = GRID_OFFSET_Y + row * (CELL_SIZE + CELL_PADDING) + CELL_PADDING
        self.target_x = self.x
        self.target_y = self.y
        
    def set_target(self, row, col):
        """Set target position for movement animation"""
        self.target_row = row
        self.target_col = col
        self.target_x = GRID_OFFSET_X + col * (CELL_SIZE + CELL_PADDING) + CELL_PADDING
        self.target_y = GRID_OFFSET_Y + row * (CELL_SIZE + CELL_PADDING) + CELL_PADDING
        
    def update(self, speed=0.2):
        """Update animation state"""
        # Smooth position movement
        self.x += (self.target_x - self.x) * speed
        self.y += (self.target_y - self.y) * speed
        
        # Scale animation for new tiles
        if self.is_new:
            self.scale += (self.target_scale - self.scale) * 0.15
            if abs(self.target_scale - self.scale) < 0.01:
                self.scale = self.target_scale
                self.is_new = False
                
        # Merge pulse animation
        if self.is_merging:
            self.merge_scale += (1.0 - self.merge_scale) * 0.1
            if abs(1.0 - self.merge_scale) < 0.01:
                self.is_merging = False
                self.merge_scale = 1.0
                
    def draw(self, screen, font):
        """Draw the tile"""
        if self.value == 0:
            return
            
        # Calculate actual scale
        actual_scale = self.scale * self.merge_scale
        
        # Calculate draw position with scale
        center_x = self.x + CELL_SIZE // 2
        center_y = self.y + CELL_SIZE // 2
        draw_size = int(CELL_SIZE * actual_scale)
        draw_x = center_x - draw_size // 2
        draw_y = center_y - draw_size // 2
        
        # Get color
        color = TILE_COLORS.get(self.value, (60, 58, 50))
        
        # Draw rounded rectangle
        self._draw_rounded_rect(screen, draw_x, draw_y, draw_size, draw_size, 8, color)
        
        # Draw text
        if self.value > 0:
            text_color = TEXT_COLORS.get(self.value, TEXT_LIGHT)
            text = str(self.value)
            
            # Adjust font size based on number length
            if len(text) <= 2:
                text_size = 48
            elif len(text) == 3:
                text_size = 40
            else:
                text_size = 32
                
            text_font = pygame.font.Font(None, text_size)
            text_surface = text_font.render(text, True, text_color)
            text_rect = text_surface.get_rect(center=(center_x, center_y))
            screen.blit(text_surface, text_rect)
            
    def _draw_rounded_rect(self, screen, x, y, width, height, radius, color):
        """Draw a rounded rectangle"""
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, color, rect, border_radius=radius)


class PygameUI:
    """Pygame-based graphical user interface"""
    
    def __init__(self):
        """Initialize Pygame UI"""
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("1024 Game")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
        # Animation state
        self.tiles = {}  # (row, col) -> AnimatedTile
        self.particles = []
        self.animating = False
        self.previous_grid = None
        
        # Game state
        self.game_over = False
        self.won = False
        self.show_win_overlay = False
        
    def init_tiles(self, grid):
        """Initialize tiles from grid"""
        self.tiles = {}
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                value = grid[row][col]
                if value != 0:
                    self.tiles[(row, col)] = AnimatedTile(value, row, col)
                    
    def update_tiles(self, grid, merged_positions=None, new_tile_position=None):
        """Update tiles based on new grid state"""
        new_tiles = {}
        moved = False
        
        # Track which positions have been processed
        processed = set()
        
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                value = grid[row][col]
                if value == 0:
                    continue
                    
                # Find the source of this tile
                found = False
                for (old_row, old_col), tile in self.tiles.items():
                    if (old_row, old_col) in processed:
                        continue
                    if tile.value == value or (merged_positions and (row, col) in merged_positions):
                        # Move existing tile
                        tile.set_target(row, col)
                        new_tiles[(row, col)] = tile
                        processed.add((old_row, old_col))
                        if old_row != row or old_col != col:
                            moved = True
                        found = True
                        break
                        
                if not found:
                    # Create new tile
                    is_new = (new_tile_position == (row, col))
                    new_tiles[(row, col)] = AnimatedTile(value, row, col, is_new=is_new)
                    if is_new:
                        moved = True
                        
        self.tiles = new_tiles
        
        # Mark merged tiles
        if merged_positions:
            for pos in merged_positions:
                if pos in self.tiles:
                    self.tiles[pos].is_merging = True
                    self.spawn_merge_particles(pos)
                    
        return moved
        
    def spawn_merge_particles(self, position):
        """Spawn particle effect at tile position"""
        row, col = position
        x = GRID_OFFSET_X + col * (CELL_SIZE + CELL_PADDING) + CELL_PADDING + CELL_SIZE // 2
        y = GRID_OFFSET_Y + row * (CELL_SIZE + CELL_PADDING) + CELL_PADDING + CELL_SIZE // 2
        
        # Get tile color
        value = self.tiles.get(position, AnimatedTile(2, 0, 0)).value
        color = TILE_COLORS.get(value, (255, 255, 255))
        
        # Spawn particles
        for _ in range(20):
            velocity = (random.uniform(-4, 4), random.uniform(-6, -2))
            size = random.randint(6, 14)
            self.particles.append(Particle(x, y, color, velocity, size))
            
    def spawn_new_tile_particles(self, position, value):
        """Spawn particle effect for new tile"""
        row, col = position
        x = GRID_OFFSET_X + col * (CELL_SIZE + CELL_PADDING) + CELL_PADDING + CELL_SIZE // 2
        y = GRID_OFFSET_Y + row * (CELL_SIZE + CELL_PADDING) + CELL_PADDING + CELL_SIZE // 2
        
        color = TILE_COLORS.get(value, (255, 255, 255))
        
        # Spawn ring effect
        for angle in range(0, 360, 20):
            rad = math.radians(angle)
            vx = math.cos(rad) * 3
            vy = math.sin(rad) * 3
            self.particles.append(Particle(x, y, color, (vx, vy), 8, 40))
        
    def draw_background(self):
        """Draw game background"""
        self.screen.fill(BACKGROUND_COLOR)
        
    def draw_header(self, score, high_score):
        """Draw game header with title and scores"""
        # Title
        title = self.font_large.render("1024", True, (119, 110, 101))
        self.screen.blit(title, (60, 30))
        
        # Score box
        score_box = pygame.Rect(320, 20, 110, 70)
        pygame.draw.rect(self.screen, (187, 173, 160), score_box, border_radius=6)
        score_label = self.font_small.render("SCORE", True, (238, 228, 218))
        score_label_rect = score_label.get_rect(center=(375, 40))
        self.screen.blit(score_label, score_label_rect)
        score_text = self.font_small.render(str(score), True, (255, 255, 255))
        score_text_rect = score_text.get_rect(center=(375, 65))
        self.screen.blit(score_text, score_text_rect)
        
        # High score box
        high_score_box = pygame.Rect(440, 20, 110, 70)
        pygame.draw.rect(self.screen, (187, 173, 160), high_score_box, border_radius=6)
        high_score_label = self.font_small.render("BEST", True, (238, 228, 218))
        high_score_label_rect = high_score_label.get_rect(center=(495, 40))
        self.screen.blit(high_score_label, high_score_label_rect)
        high_score_text = self.font_small.render(str(high_score), True, (255, 255, 255))
        high_score_text_rect = high_score_text.get_rect(center=(495, 65))
        self.screen.blit(high_score_text, high_score_text_rect)
        
        # Subtitle
        subtitle = self.font_small.render("Join the numbers, get to 1024!", True, (119, 110, 101))
        self.screen.blit(subtitle, (60, 100))
        
        # New Game button
        new_game_btn = pygame.Rect(380, 100, 160, 40)
        pygame.draw.rect(self.screen, (143, 122, 102), new_game_btn, border_radius=6)
        new_game_text = self.font_small.render("New Game", True, (255, 255, 255))
        new_game_text_rect = new_game_text.get_rect(center=(460, 120))
        self.screen.blit(new_game_text, new_game_text_rect)
        
        return new_game_btn
        
    def draw_grid_background(self):
        """Draw the grid background"""
        grid_rect = pygame.Rect(
            GRID_OFFSET_X, 
            GRID_OFFSET_Y, 
            GRID_SIZE * (CELL_SIZE + CELL_PADDING) + CELL_PADDING,
            GRID_SIZE * (CELL_SIZE + CELL_PADDING) + CELL_PADDING
        )
        pygame.draw.rect(self.screen, GRID_BACKGROUND, grid_rect, border_radius=10)
        
        # Draw empty cells
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = GRID_OFFSET_X + col * (CELL_SIZE + CELL_PADDING) + CELL_PADDING
                y = GRID_OFFSET_Y + row * (CELL_SIZE + CELL_PADDING) + CELL_PADDING
                cell_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, CELL_EMPTY, cell_rect, border_radius=6)
                
    def draw_tiles(self):
        """Draw all tiles"""
        for tile in self.tiles.values():
            tile.draw(self.screen, self.font_medium)
            
    def draw_particles(self):
        """Draw and update particles"""
        for particle in self.particles[:]:
            if particle.update():
                particle.draw(self.screen)
            else:
                self.particles.remove(particle)
                
    def draw_game_over_overlay(self, score):
        """Draw game over overlay"""
        # Semi-transparent background
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 200))
        self.screen.blit(overlay, (0, 0))
        
        # Game Over box
        box_rect = pygame.Rect(100, 250, 400, 250)
        pygame.draw.rect(self.screen, (187, 173, 160), box_rect, border_radius=10)
        
        # Text
        game_over_text = self.font_large.render("Game Over!", True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(center=(300, 320))
        self.screen.blit(game_over_text, game_over_rect)
        
        score_text = self.font_medium.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(300, 380))
        self.screen.blit(score_text, score_rect)
        
        # Try Again button
        try_again_btn = pygame.Rect(200, 420, 200, 50)
        pygame.draw.rect(self.screen, (143, 122, 102), try_again_btn, border_radius=6)
        try_again_text = self.font_small.render("Try Again", True, (255, 255, 255))
        try_again_rect = try_again_text.get_rect(center=(300, 445))
        self.screen.blit(try_again_text, try_again_rect)
        
        return try_again_btn
        
    def draw_win_overlay(self, score):
        """Draw win overlay"""
        # Semi-transparent background
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 200))
        self.screen.blit(overlay, (0, 0))
        
        # Win box
        box_rect = pygame.Rect(100, 250, 400, 250)
        pygame.draw.rect(self.screen, (237, 197, 63), box_rect, border_radius=10)
        
        # Text
        win_text = self.font_large.render("You Win!", True, (255, 255, 255))
        win_rect = win_text.get_rect(center=(300, 320))
        self.screen.blit(win_text, win_rect)
        
        score_text = self.font_medium.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(300, 380))
        self.screen.blit(score_text, score_rect)
        
        # Continue button
        continue_btn = pygame.Rect(200, 420, 200, 50)
        pygame.draw.rect(self.screen, (143, 122, 102), continue_btn, border_radius=6)
        continue_text = self.font_small.render("Continue", True, (255, 255, 255))
        continue_rect = continue_text.get_rect(center=(300, 445))
        self.screen.blit(continue_text, continue_rect)
        
        return continue_btn
        
    def draw_controls(self):
        """Draw control instructions"""
        controls_text = [
            "Controls: Arrow Keys or WASD to move",
            "Press R to restart, ESC to quit"
        ]
        y = WINDOW_HEIGHT - 60
        for text in controls_text:
            control_surface = self.font_small.render(text, True, (119, 110, 101))
            control_rect = control_surface.get_rect(center=(WINDOW_WIDTH // 2, y))
            self.screen.blit(control_surface, control_rect)
            y += 25
            
    def update_animations(self):
        """Update all animations"""
        self.animating = False
        for tile in self.tiles.values():
            tile.update()
            # Check if still animating
            if abs(tile.x - tile.target_x) > 0.5 or abs(tile.y - tile.target_y) > 0.5:
                self.animating = True
            if tile.is_new or tile.is_merging:
                self.animating = True
                
    def draw(self, game):
        """Draw complete game state"""
        self.draw_background()
        new_game_btn = self.draw_header(game.get_score(), game.get_high_score())
        self.draw_grid_background()
        self.draw_tiles()
        self.draw_particles()
        self.draw_controls()
        
        try_again_btn = None
        continue_btn = None
        
        if self.game_over:
            try_again_btn = self.draw_game_over_overlay(game.get_score())
        elif self.show_win_overlay:
            continue_btn = self.draw_win_overlay(game.get_score())
            
        pygame.display.flip()
        
        return new_game_btn, try_again_btn, continue_btn
        
    def get_direction_from_key(self, key):
        """Convert key press to direction"""
        if key in [pygame.K_UP, pygame.K_w]:
            return 'up'
        elif key in [pygame.K_DOWN, pygame.K_s]:
            return 'down'
        elif key in [pygame.K_LEFT, pygame.K_a]:
            return 'left'
        elif key in [pygame.K_RIGHT, pygame.K_d]:
            return 'right'
        return None
        
    def run(self, game):
        """Main game loop"""
        self.init_tiles(game.get_grid())
        self.previous_grid = game.get_grid()
        
        running = True
        move_in_progress = False
        
        while running:
            new_game_btn = None
            try_again_btn = None
            continue_btn = None
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r:
                        game.reset_game()
                        self.init_tiles(game.get_grid())
                        self.previous_grid = game.get_grid()
                        self.game_over = False
                        self.won = False
                        self.show_win_overlay = False
                    elif not self.game_over and not self.show_win_overlay:
                        direction = self.get_direction_from_key(event.key)
                        if direction:
                            self.previous_grid = game.get_grid()
                            if game.move(direction):
                                move_in_progress = True
                                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        mouse_pos = event.pos
                        if new_game_btn and new_game_btn.collidepoint(mouse_pos):
                            game.reset_game()
                            self.init_tiles(game.get_grid())
                            self.previous_grid = game.get_grid()
                            self.game_over = False
                            self.won = False
                            self.show_win_overlay = False
                        elif try_again_btn and try_again_btn.collidepoint(mouse_pos):
                            game.reset_game()
                            self.init_tiles(game.get_grid())
                            self.previous_grid = game.get_grid()
                            self.game_over = False
                            self.won = False
                            self.show_win_overlay = False
                        elif continue_btn and continue_btn.collidepoint(mouse_pos):
                            self.show_win_overlay = False
                            
            # Handle move completion
            if move_in_progress and not self.animating:
                # Add new tile
                new_pos = game.add_random_tile()
                if new_pos:
                    row, col = new_pos
                    value = game.get_grid()[row][col]
                    self.spawn_new_tile_particles((row, col), value)
                    
                # Update tiles
                self.update_tiles(game.get_grid(), new_tile_position=new_pos)
                move_in_progress = False
                
                # Check win/lose conditions
                if game.is_win() and not self.won:
                    self.won = True
                    self.show_win_overlay = True
                elif game.is_game_over():
                    self.game_over = True
                    
            # Update animations
            self.update_animations()
            
            # Draw
            new_game_btn, try_again_btn, continue_btn = self.draw(game)
            
            # Cap framerate
            self.clock.tick(60)
            
        game.save_high_score()
        pygame.quit()


def main():
    """Main entry point"""
    try:
        game = Game()
        ui = PygameUI()
        ui.run(game)
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

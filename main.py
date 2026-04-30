"""
<<<<<<< HEAD
Road Builder Game - A Logical Road Building Puzzle Game
Based on Task 1 Coursework Requirements

Game Features:
- 4x4 Grid Game Board (matching Task 1's 4 road builders concept)
- 4 Challenge Levels
- Physics-based vehicle movement
- Bridge/Road piece placement
- Cost-based scoring system

Author: WindSongShaoGe
=======
Road Builder Game - A Logical Road Builder Puzzle with Physics
Built with Python + Pygame

This game meets the following Task 1 requirements:
- 4x4 game board (4 blocks of 3.75" equivalent)
- 4 challenge levels
- Vehicle movement from start to end
- Accessory placement logic
- Vehicle animation
- Win detection
>>>>>>> f56e601d65e2c24e33985b9b1302c9416529a868
"""

import pygame
import sys
<<<<<<< HEAD
import math
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional


# ============================================================
# CONSTANTS & CONFIGURATION
# ============================================================
=======
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional
import json


# ============== Constants ==============
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
GRID_SIZE = 4  # 4x4 grid
CELL_SIZE = 120
GRID_OFFSET_X = 50
GRID_OFFSET_Y = 100
>>>>>>> f56e601d65e2c24e33985b9b1302c9416529a868

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)
<<<<<<< HEAD
GREEN = (34, 139, 34)
BLUE = (30, 144, 255)
=======
BLUE = (70, 130, 180)
GREEN = (34, 139, 34)
>>>>>>> f56e601d65e2c24e33985b9b1302c9416529a868
RED = (220, 20, 60)
YELLOW = (255, 215, 0)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)
SKY_BLUE = (135, 206, 235)

<<<<<<< HEAD
# Game Dimensions
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
GRID_SIZE = 4  # 4x4 grid (matching Task 1's 4 road builders)
CELL_SIZE = 120  # Each cell is 120x120 pixels
GRID_OFFSET_X = 50
GRID_OFFSET_Y = 100

# UI Elements
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 40
SIDEBAR_WIDTH = 250

# Game States
class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    RUNNING = "running"  # Vehicle is moving
    WIN = "win"
    LOSE = "lose"


# ============================================================
# DATA STRUCTURES
# ============================================================

@dataclass
class Position:
    """Represents a position on the grid"""
    row: int
    col: int
    
    def to_pixel(self) -> Tuple[int, int]:
        """Convert grid position to pixel position (center of cell)"""
        x = GRID_OFFSET_X + self.col * CELL_SIZE + CELL_SIZE // 2
        y = GRID_OFFSET_Y + self.row * CELL_SIZE + CELL_SIZE // 2
        return (x, y)
    
    def is_valid(self) -> bool:
        """Check if position is within grid bounds"""
        return 0 <= self.row < GRID_SIZE and 0 <= self.col < GRID_SIZE


class PieceType(Enum):
    """Types of road/bridge pieces available"""
    EMPTY = 0
    ROAD_HORIZONTAL = 1    # Horizontal road
    ROAD_VERTICAL = 2      # Vertical road
    ROAD_TURN_BR = 3       # Turn: Bottom to Right
    ROAD_TURN_BL = 4       # Turn: Bottom to Left
    ROAD_TURN_TR = 5       # Turn: Top to Right
    ROAD_TURN_TL = 6       # Turn: Top to Left
    BRIDGE_SHORT = 7       # Short bridge (2 cells)
    BRIDGE_LONG = 8        # Long bridge (3 cells)
    RAMP_UP = 9            # Ramp going up
    RAMP_DOWN = 10         # Ramp going down


@dataclass
class Piece:
    """Represents a road/bridge piece"""
    piece_type: PieceType
    cost: float  # Cost for scoring
    connections: List[str]  # ['top', 'bottom', 'left', 'right']
    
    @staticmethod
    def get_piece_info(piece_type: PieceType) -> 'Piece':
        """Get piece information based on type"""
        pieces_info = {
            PieceType.ROAD_HORIZONTAL: Piece(
                piece_type, 10, ['left', 'right']
            ),
            PieceType.ROAD_VERTICAL: Piece(
                piece_type, 10, ['top', 'bottom']
            ),
            PieceType.ROAD_TURN_BR: Piece(
                piece_type, 15, ['bottom', 'right']
            ),
            PieceType.ROAD_TURN_BL: Piece(
                piece_type, 15, ['bottom', 'left']
            ),
            PieceType.ROAD_TURN_TR: Piece(
                piece_type, 15, ['top', 'right']
            ),
            PieceType.ROAD_TURN_TL: Piece(
                piece_type, 15, ['top', 'left']
            ),
            PieceType.BRIDGE_SHORT: Piece(
                piece_type, 25, ['left', 'right']
            ),
            PieceType.BRIDGE_LONG: Piece(
                piece_type, 35, ['left', 'right']
            ),
            PieceType.RAMP_UP: Piece(
                piece_type, 20, ['bottom', 'top']
            ),
            PieceType.RAMP_DOWN: Piece(
                piece_type, 20, ['top', 'bottom']
            ),
        }
        return pieces_info.get(piece_type, Piece(piece_type, 0, []))


class Vehicle:
    """Represents the vehicle that moves on the road"""
    
    def __init__(self, start_pos: Position):
        self.position = start_pos
        self.target_position: Optional[Position] = None
        self.direction = 'right'  # 'up', 'down', 'left', 'right'
        self.speed = 3
        self.is_moving = False
        self.path: List[Position] = []
        self.path_index = 0
        self.animation_progress = 0.0
        
    def set_path(self, path: List[Position]):
        """Set the path for the vehicle to follow"""
        self.path = path
        self.path_index = 0
        if len(path) > 1:
            self.is_moving = True
            self.target_position = path[1]
            self._update_direction()
    
    def _update_direction(self):
        """Update direction based on target position"""
        if self.target_position and self.position:
            dr = self.target_position.row - self.position.row
            dc = self.target_position.col - self.position.col
            if dr < 0:
                self.direction = 'up'
            elif dr > 0:
                self.direction = 'down'
            elif dc < 0:
                self.direction = 'left'
            elif dc > 0:
                self.direction = 'right'
    
    def update(self):
        """Update vehicle position (called every frame)"""
        if not self.is_moving or not self.target_position:
            return
            
        self.animation_progress += self.speed / CELL_SIZE
        
        if self.animation_progress >= 1.0:
            # Reached target
            self.position = self.target_position
            self.animation_progress = 0.0
            self.path_index += 1
            
            if self.path_index < len(self.path) - 1:
                self.target_position = self.path[self.path_index + 1]
                self._update_direction()
            else:
                # Reached end of path
                self.is_moving = False
                self.target_position = None
    
    def get_current_pixel_pos(self) -> Tuple[int, int]:
        """Get current pixel position with animation"""
        if not self.target_position or not self.position:
            return self.position.to_pixel() if self.position else (0, 0)
        
        start_x, start_y = self.position.to_pixel()
        target_x, target_y = self.target_position.to_pixel()
        
        # Interpolate based on animation progress
        x = start_x + (target_x - start_x) * self.animation_progress
        y = start_y + (target_y - start_y) * self.animation_progress
        
        return (int(x), int(y))
=======
# Road/Bridge colors
ROAD_COLOR = (80, 80, 80)
BRIDGE_COLOR = (160, 120, 80)
WATER_COLOR = (30, 144, 255)


class ComponentType(Enum):
    """Types of road components players can place"""
    ROAD = "road"           # Normal road
    BRIDGE = "bridge"       # Bridge over water
    RAMP = "ramp"           # Ramp for elevation


class CellType(Enum):
    """Types of cells on the game board"""
    GRASS = "grass"         # Empty, cannot drive on
    ROAD = "road"           # Normal road
    WATER = "water"         # Needs bridge
    START = "start"         # Starting position
    END = "end"             # Destination
    OBSTACLE = "obstacle"   # Cannot place anything here
>>>>>>> f56e601d65e2c24e33985b9b1302c9416529a868


@dataclass
class Challenge:
    """Represents a game challenge/level"""
    name: str
<<<<<<< HEAD
    start_pos: Position
    end_pos: Position
    available_pieces: List[Tuple[PieceType, int]]  # (piece_type, quantity)
    obstacles: List[Position]  # Positions with obstacles
    par_score: int  # Target score for 3 stars


# ============================================================
# GAME CLASS
# ============================================================

class RoadBuilderGame:
    """Main game class"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Road Builder Game - Logical Road Puzzle")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game state
        self.state = GameState.MENU
        self.current_level = 0
        self.total_cost = 0.0
        
        # Grid: 2D array storing piece types
        self.grid: List[List[PieceType]] = [
            [PieceType.EMPTY for _ in range(GRID_SIZE)]
            for _ in range(GRID_SIZE)
        ]
        
        # Selected piece for placement
        self.selected_piece: Optional[PieceType] = None
        
        # Vehicle
        self.vehicle: Optional[Vehicle] = None
        
        # Challenges
        self.challenges = self._create_challenges()
        
        # Available pieces for current level
        self.available_pieces: List[Tuple[PieceType, int]] = []
        
        # Mouse interaction
        self.hovered_cell: Optional[Position] = None
        
    def _create_challenges(self) -> List[Challenge]:
        """Create 4 challenge levels"""
        return [
            Challenge(
                name="Level 1: Basic Road",
                start_pos=Position(0, 0),
                end_pos=Position(3, 3),
                available_pieces=[
                    (PieceType.ROAD_HORIZONTAL, 10),
                    (PieceType.ROAD_VERTICAL, 10),
                    (PieceType.ROAD_TURN_BR, 2),
                    (PieceType.ROAD_TURN_BL, 2),
                    (PieceType.ROAD_TURN_TR, 2),
                    (PieceType.ROAD_TURN_TL, 2),
                ],
                obstacles=[],
                par_score=50
            ),
            Challenge(
                name="Level 2: The Gap",
                start_pos=Position(0, 0),
                end_pos=Position(3, 3),
                available_pieces=[
                    (PieceType.ROAD_HORIZONTAL, 8),
                    (PieceType.ROAD_VERTICAL, 8),
                    (PieceType.ROAD_TURN_BR, 3),
                    (PieceType.ROAD_TURN_BL, 3),
                    (PieceType.ROAD_TURN_TR, 3),
                    (PieceType.ROAD_TURN_TL, 3),
                    (PieceType.BRIDGE_SHORT, 2),
                ],
                obstacles=[Position(1, 1), Position(2, 2)],
                par_score=80
            ),
            Challenge(
                name="Level 3: Maze Runner",
                start_pos=Position(0, 0),
                end_pos=Position(3, 3),
                available_pieces=[
                    (PieceType.ROAD_HORIZONTAL, 6),
                    (PieceType.ROAD_VERTICAL, 6),
                    (PieceType.ROAD_TURN_BR, 4),
                    (PieceType.ROAD_TURN_BL, 4),
                    (PieceType.ROAD_TURN_TR, 4),
                    (PieceType.ROAD_TURN_TL, 4),
                    (PieceType.BRIDGE_SHORT, 3),
                    (PieceType.BRIDGE_LONG, 2),
                ],
                obstacles=[Position(0, 2), Position(1, 1), Position(2, 0), Position(3, 1)],
                par_score=100
            ),
            Challenge(
                name="Level 4: The Challenge",
                start_pos=Position(0, 0),
                end_pos=Position(3, 3),
                available_pieces=[
                    (PieceType.ROAD_HORIZONTAL, 5),
                    (PieceType.ROAD_VERTICAL, 5),
                    (PieceType.ROAD_TURN_BR, 5),
                    (PieceType.ROAD_TURN_BL, 5),
                    (PieceType.ROAD_TURN_TR, 5),
                    (PieceType.ROAD_TURN_TL, 5),
                    (PieceType.BRIDGE_SHORT, 3),
                    (PieceType.BRIDGE_LONG, 3),
                    (PieceType.RAMP_UP, 2),
                    (PieceType.RAMP_DOWN, 2),
                ],
                obstacles=[Position(0, 1), Position(1, 0), Position(1, 2), Position(2, 1), Position(2, 3)],
                par_score=120
            ),
        ]
    
    def load_level(self, level_index: int):
        """Load a specific level"""
        if 0 <= level_index < len(self.challenges):
            self.current_level = level_index
            challenge = self.challenges[level_index]
            
            # Reset grid
            self.grid = [
                [PieceType.EMPTY for _ in range(GRID_SIZE)]
                for _ in range(GRID_SIZE)
            ]
            
            # Set obstacles
            for obs in challenge.obstacles:
                self.grid[obs.row][obs.col] = None  # Mark as obstacle
            
            # Copy available pieces
            self.available_pieces = challenge.available_pieces.copy()
            
            # Create vehicle at start position
            self.vehicle = Vehicle(challenge.start_pos)
            
            # Reset cost
            self.total_cost = 0.0
            
            self.state = GameState.PLAYING
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            self.clock.tick(60)
            
=======
    difficulty: str
    grid: List[List[str]]  # Cell types
    start_pos: Tuple[int, int]
    end_pos: Tuple[int, int]
    max_cost: int


class RoadBuilderGame:
    """Main game class"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Road Builder Game - Logical Road Builder")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # Game state
        self.current_level = 0
        self.game_state = "playing"  # playing, running, win, lose
        self.placed_components = {}  # (row, col) -> ComponentType
        self.total_cost = 0
        self.vehicle_pos = None
        self.vehicle_path = []
        self.animation_index = 0
        self.message = ""
        self.score = 0

        # Initialize challenges
        self.challenges = self.create_challenges()
        self.load_level(0)

    def create_challenges(self) -> List[Challenge]:
        """Create 4 challenge levels"""
        challenges = []

        # Level 1: Simple - One water gap
        level1 = Challenge(
            name="Level 1: First Bridge",
            difficulty="Easy",
            grid=[
                ["grass", "road", "road", "grass"],
                ["grass", "grass", "water", "grass"],
                ["grass", "grass", "water", "grass"],
                ["grass", "road", "road", "end"]
            ],
            start_pos=(0, 1),
            end_pos=(3, 3),
            max_cost=200
        )
        challenges.append(level1)

        # Level 2: Medium - Two water gaps
        level2 = Challenge(
            name="Level 2: Double Crossing",
            difficulty="Medium",
            grid=[
                ["start", "road", "water", "grass"],
                ["grass", "grass", "water", "grass"],
                ["grass", "road", "road", "water"],
                ["grass", "grass", "grass", "end"]
            ],
            start_pos=(0, 0),
            end_pos=(3, 3),
            max_cost=300
        )
        challenges.append(level2)

        # Level 3: Hard - Multiple obstacles
        level3 = Challenge(
            name="Level 3: Maze Runner",
            difficulty="Hard",
            grid=[
                ["start", "water", "road", "grass"],
                ["grass", "water", "grass", "road"],
                ["road", "grass", "water", "grass"],
                ["grass", "road", "road", "end"]
            ],
            start_pos=(0, 0),
            end_pos=(3, 3),
            max_cost=400
        )
        challenges.append(level3)

        # Level 4: Expert - Complex path
        level4 = Challenge(
            name="Level 4: Master Builder",
            difficulty="Expert",
            grid=[
                ["start", "road", "water", "road", "water"],
                ["water", "grass", "water", "grass", "road"],
                ["road", "water", "road", "grass", "water"],
                ["grass", "road", "grass", "water", "road"],
                ["water", "grass", "road", "road", "end"]
            ],
            start_pos=(0, 0),
            end_pos=(4, 4),
            max_cost=500
        )
        challenges.append(level4)

        return challenges

    def load_level(self, level_index: int):
        """Load a specific challenge level"""
        self.current_level = level_index
        self.placed_components = {}
        self.total_cost = 0
        self.game_state = "playing"
        self.vehicle_pos = list(self.challenges[level_index].start_pos)
        self.vehicle_path = []
        self.animation_index = 0
        self.message = f"Level {level_index + 1}: {self.challenges[level_index].name}"

    def get_grid_size(self) -> int:
        """Get current level grid size"""
        return len(self.challenges[self.current_level].grid)

    def get_cell_type(self, row: int, col: int) -> CellType:
        """Get the type of cell at position"""
        challenge = self.challenges[self.current_level]
        if row < 0 or row >= len(challenge.grid) or col < 0 or col >= len(challenge.grid[0]):
            return CellType.OBSTACLE

        cell_str = challenge.grid[row][col].lower()
        if cell_str == "grass":
            return CellType.GRASS
        elif cell_str == "road":
            return CellType.ROAD
        elif cell_str == "water":
            return CellType.WATER
        elif cell_str == "start":
            return CellType.START
        elif cell_str == "end":
            return CellType.END
        elif cell_str == "obstacle":
            return CellType.OBSTACLE
        return CellType.GRASS

    def handle_click(self, pos: Tuple[int, int]):
        """Handle mouse click events"""
        if self.game_state != "playing":
            return

        # Check if click is on UI buttons
        buttons = self.get_buttons()
        for btn_rect, btn_action in buttons:
            if btn_rect.collidepoint(pos):
                btn_action()
                return

        # Check if click is on grid
        grid_size = self.get_grid_size()
        for row in range(grid_size):
            for col in range(grid_size):
                cell_x = GRID_OFFSET_X + col * CELL_SIZE
                cell_y = GRID_OFFSET_Y + row * CELL_SIZE
                cell_rect = pygame.Rect(cell_x, cell_y, CELL_SIZE, CELL_SIZE)

                if cell_rect.collidepoint(pos):
                    self.handle_grid_click(row, col)

    def handle_grid_click(self, row: int, col: int):
        """Handle click on grid cell"""
        cell_type = self.get_cell_type(row, col)

        # Check if this is start or end position
        challenge = self.challenges[self.current_level]
        if (row, col) == challenge.start_pos or (row, col) == challenge.end_pos:
            self.message = "Cannot place on start/end!"
            return

        # Handle water cells - need bridge
        if cell_type == CellType.WATER:
            if (row, col) in self.placed_components:
                del self.placed_components[(row, col)]
                self.total_cost -= 50
                self.message = "Bridge removed (-$50)"
            else:
                self.placed_components[(row, col)] = ComponentType.BRIDGE
                self.total_cost += 50
                self.message = "Bridge placed (+$50)"
            return

        # Handle grass cells - can place road
        if cell_type == CellType.GRASS:
            if (row, col) in self.placed_components:
                del self.placed_components[(row, col)]
                self.total_cost -= 30
                self.message = "Road removed (-$30)"
            else:
                self.placed_components[(row, col)] = ComponentType.ROAD
                self.total_cost += 30
                self.message = "Road placed (+$30)"
            return

        self.message = "Cannot place here!"

    def get_buttons(self) -> List[Tuple[pygame.Rect, callable]]:
        """Get all UI buttons"""
        buttons = []

        # Start button
        start_btn = pygame.Rect(650, 150, 150, 50)
        buttons.append((start_btn, self.start_simulation))

        # Reset button
        reset_btn = pygame.Rect(650, 220, 150, 50)
        buttons.append((reset_btn, self.reset_level))

        # Level buttons
        for i in range(4):
            level_btn = pygame.Rect(50 + i * 200, 30, 180, 40)
            buttons.append((level_btn, lambda idx=i: self.load_level(idx)))

        return buttons

    def start_simulation(self):
        """Start the vehicle simulation"""
        if self.game_state != "playing":
            return

        # Find path
        path = self.find_path()
        if path:
            self.vehicle_path = path
            self.animation_index = 0
            self.game_state = "running"
            self.message = "Simulation running..."
        else:
            self.game_state = "lose"
            self.message = "No valid path! Try again."

    def find_path(self) -> Optional[List[Tuple[int, int]]]:
        """Find a valid path from start to end using BFS"""
        challenge = self.challenges[self.current_level]
        start = challenge.start_pos
        end = challenge.end_pos
        grid_size = self.get_grid_size()

        # BFS
        queue = [[start]]
        visited = {start}

        while queue:
            path = queue.pop(0)
            current = path[-1]

            if current == end:
                return path

            # Check all 4 directions
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for dx, dy in directions:
                next_pos = (current[0] + dx, current[1] + dy)

                if (next_pos in visited or
                    next_pos[0] < 0 or next_pos[0] >= grid_size or
                    next_pos[1] < 0 or next_pos[1] >= grid_size):
                    continue

                # Check if can move to this cell
                if self.can_move_to(next_pos):
                    visited.add(next_pos)
                    new_path = path + [next_pos]
                    queue.append(new_path)

        return None

    def can_move_to(self, pos: Tuple[int, int]) -> bool:
        """Check if vehicle can move to position"""
        row, col = pos
        cell_type = self.get_cell_type(row, col)

        # Check placed components
        if pos in self.placed_components:
            return True

        # Check if it's a road, start, or end
        if cell_type in [CellType.ROAD, CellType.START, CellType.END]:
            return True

        return False

    def update_animation(self):
        """Update vehicle animation"""
        if self.game_state == "running" and self.vehicle_path:
            self.animation_index += 0.05
            if self.animation_index >= len(self.vehicle_path) - 1:
                self.animation_index = len(self.vehicle_path) - 1
                self.game_state = "win"
                self.calculate_score()
                self.message = "You Win! Vehicle reached the destination!"

    def calculate_score(self):
        """Calculate score based on cost"""
        challenge = self.challenges[self.current_level]
        max_cost = challenge.max_cost

        # Lower cost = higher score
        if self.total_cost <= max_cost:
            self.score = int(100 * (1 - self.total_cost / max_cost) + 50)
        else:
            self.score = max(0, 50 - (self.total_cost - max_cost) // 10)

    def reset_level(self):
        """Reset current level"""
        self.load_level(self.current_level)
        self.message = "Level reset!"

    def draw(self):
        """Draw the game"""
        self.screen.fill(WHITE)

        # Draw title
        title = self.font.render("Road Builder Game", True, BLACK)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 10))

        # Draw level buttons
        for i in range(4):
            btn_rect = pygame.Rect(50 + i * 200, 30, 180, 40)
            color = BLUE if i == self.current_level else GRAY
            pygame.draw.rect(self.screen, color, btn_rect)
            pygame.draw.rect(self.screen, BLACK, btn_rect, 2)
            level_text = self.small_font.render(f"Level {i+1}", True, WHITE)
            self.screen.blit(level_text, (btn_rect.x + 60, btn_rect.y + 10))

        # Draw grid
        self.draw_grid()

        # Draw vehicle
        self.draw_vehicle()

        # Draw UI
        self.draw_ui()

        pygame.display.flip()

    def draw_grid(self):
        """Draw the game grid"""
        challenge = self.challenges[self.current_level]
        grid_size = self.get_grid_size()

        for row in range(grid_size):
            for col in range(grid_size):
                cell_x = GRID_OFFSET_X + col * CELL_SIZE
                cell_y = GRID_OFFSET_Y + row * CELL_SIZE

                cell_type = self.get_cell_type(row, col)
                rect = pygame.Rect(cell_x, cell_y, CELL_SIZE, CELL_SIZE)

                # Draw base cell
                if cell_type == CellType.WATER:
                    pygame.draw.rect(self.screen, WATER_COLOR, rect)
                elif cell_type == CellType.GRASS:
                    pygame.draw.rect(self.screen, GREEN, rect)
                elif cell_type == CellType.ROAD:
                    pygame.draw.rect(self.screen, ROAD_COLOR, rect)
                elif cell_type == CellType.START:
                    pygame.draw.rect(self.screen, BLUE, rect)
                elif cell_type == CellType.END:
                    pygame.draw.rect(self.screen, RED, rect)
                else:
                    pygame.draw.rect(self.screen, DARK_GRAY, rect)

                # Draw grid lines
                pygame.draw.rect(self.screen, BLACK, rect, 2)

                # Draw placed components
                if (row, col) in self.placed_components:
                    comp = self.placed_components[(row, col)]
                    if comp == ComponentType.BRIDGE:
                        # Draw bridge
                        bridge_rect = rect.inflate(-20, -20)
                        pygame.draw.rect(self.screen, BROWN, bridge_rect)
                        pygame.draw.rect(self.screen, ORANGE, bridge_rect, 3)
                    elif comp == ComponentType.ROAD:
                        # Draw road
                        road_rect = rect.inflate(-20, -20)
                        pygame.draw.rect(self.screen, ROAD_COLOR, road_rect)
                        pygame.draw.rect(self.screen, YELLOW, road_rect, 2)

                # Draw start/end labels
                if cell_type == CellType.START:
                    label = self.small_font.render("START", True, WHITE)
                    self.screen.blit(label, (cell_x + 30, cell_y + 50))
                elif cell_type == CellType.END:
                    label = self.small_font.render("END", True, WHITE)
                    self.screen.blit(label, (cell_x + 40, cell_y + 50))

    def draw_vehicle(self):
        """Draw the vehicle"""
        if not self.vehicle_path:
            # Draw at start position
            challenge = self.challenges[self.current_level]
            start = challenge.start_pos
            pos = start
        else:
            # Animate along path
            idx = int(self.animation_index)
            if idx >= len(self.vehicle_path):
                idx = len(self.vehicle_path) - 1
            pos = self.vehicle_path[idx]

        cell_x = GRID_OFFSET_X + pos[1] * CELL_SIZE + CELL_SIZE // 2
        cell_y = GRID_OFFSET_Y + pos[0] * CELL_SIZE + CELL_SIZE // 2

        # Draw car
        car_color = RED
        car_rect = pygame.Rect(cell_x - 20, cell_y - 15, 40, 30)
        pygame.draw.rect(self.screen, car_color, car_rect)
        pygame.draw.rect(self.screen, BLACK, car_rect, 2)

        # Draw wheels
        pygame.draw.circle(self.screen, BLACK, (cell_x - 15, cell_y + 15), 5)
        pygame.draw.circle(self.screen, BLACK, (cell_x + 15, cell_y + 15), 5)

    def draw_ui(self):
        """Draw UI elements"""
        challenge = self.challenges[self.current_level]

        # Cost display
        cost_text = self.font.render(f"Cost: ${self.total_cost}", True, BLACK)
        self.screen.blit(cost_text, (650, 100))

        # Max cost
        max_cost_text = self.small_font.render(f"Max: ${challenge.max_cost}", True, GRAY)
        self.screen.blit(max_cost_text, (650, 130))

        # Buttons
        # Start button
        start_btn = pygame.Rect(650, 150, 150, 50)
        pygame.draw.rect(self.screen, GREEN, start_btn)
        pygame.draw.rect(self.screen, BLACK, start_btn, 2)
        start_text = self.font.render("START", True, WHITE)
        self.screen.blit(start_text, (700, 160))

        # Reset button
        reset_btn = pygame.Rect(650, 220, 150, 50)
        pygame.draw.rect(self.screen, ORANGE, reset_btn)
        pygame.draw.rect(self.screen, BLACK, reset_btn, 2)
        reset_text = self.font.render("RESET", True, WHITE)
        self.screen.blit(reset_text, (705, 230))

        # Score display (when win)
        if self.game_state == "win":
            score_text = self.font.render(f"Score: {self.score}", True, BLUE)
            self.screen.blit(score_text, (650, 300))

        # Message
        msg_text = self.small_font.render(self.message, True, BLACK)
        self.screen.blit(msg_text, (50, SCREEN_HEIGHT - 40))

        # Instructions
        instr = self.small_font.render("Click grass to build road ($30), water to build bridge ($50)", True, GRAY)
        self.screen.blit(instr, (50, SCREEN_HEIGHT - 20))

    def run(self):
        """Main game loop"""
        running = True

        while running:
>>>>>>> f56e601d65e2c24e33985b9b1302c9416529a868
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
<<<<<<< HEAD
                    self._handle_mouse_click(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    self._handle_mouse_motion(event.pos)
                elif event.type == pygame.KEYDOWN:
                    self._handle_keyboard(event.key)
            
            self._update()
            self._draw()
        
        pygame.quit()
        sys.exit()
    
    def _handle_mouse_click(self, pos: Tuple[int, int]):
        """Handle mouse click events"""
        if self.state == GameState.MENU:
            self._handle_menu_click(pos)
        elif self.state == GameState.PLAYING:
            self._handle_game_click(pos)
        elif self.state == GameState.WIN or self.state == GameState.LOSE:
            self._handle_result_click(pos)
    
    def _handle_menu_click(self, pos: Tuple[int, int]):
        """Handle clicks on menu screen"""
        # Check level buttons
        button_y = 250
        for i in range(4):
            if (200 <= pos[0] <= 700 and 
                button_y <= pos[1] <= button_y + 50):
                self.load_level(i)
                return
            button_y += 70
    
    def _handle_game_click(self, pos: Tuple[int, int]):
        """Handle clicks during gameplay"""
        # Check if click is on grid
        if (GRID_OFFSET_X <= pos[0] < GRID_OFFSET_X + GRID_SIZE * CELL_SIZE and
            GRID_OFFSET_Y <= pos[1] < GRID_OFFSET_Y + GRID_SIZE * CELL_SIZE):
            
            col = (pos[0] - GRID_OFFSET_X) // CELL_SIZE
            row = (pos[1] - GRID_OFFSET_Y) // CELL_SIZE
            clicked_pos = Position(row, col)
            
            # Check if valid cell and no obstacle
            challenge = self.challenges[self.current_level]
            if clicked_pos.is_valid() and clicked_pos not in challenge.obstacles:
                if self.grid[row][col] == PieceType.EMPTY and self.selected_piece:
                    # Place piece
                    self.grid[row][col] = self.selected_piece
                    # Add cost
                    piece_info = Piece.get_piece_info(self.selected_piece)
                    self.total_cost += piece_info.cost
        
        # Check piece selection buttons (right side)
        button_start_x = GRID_OFFSET_X + GRID_SIZE * CELL_SIZE + 30
        button_start_y = 150
        for i, (piece_type, count) in enumerate(self.available_pieces):
            if count > 0:
                piece_rect = pygame.Rect(button_start_x, button_start_y + i * 45, 180, 40)
                if piece_rect.collidepoint(pos):
                    self.selected_piece = piece_type
                    return
        
        # Check Run button
        run_button = pygame.Rect(GRID_OFFSET_X + GRID_SIZE * CELL_SIZE + 30, 
                                SCREEN_HEIGHT - 150, 150, 45)
        if run_button.collidepoint(pos):
            self._run_simulation()
        
        # Check Reset button
        reset_button = pygame.Rect(GRID_OFFSET_X + GRID_SIZE * CELL_SIZE + 30,
                                  SCREEN_HEIGHT - 90, 150, 45)
        if reset_button.collidepoint(pos):
            self.load_level(self.current_level)
    
    def _handle_result_click(self, pos: Tuple[int, int]):
        """Handle clicks on win/lose screen"""
        # Check Continue button
        continue_button = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 50, 150, 45)
        if continue_button.collidepoint(pos):
            if self.current_level < len(self.challenges) - 1:
                self.load_level(self.current_level + 1)
            else:
                self.state = GameState.MENU
    
    def _handle_mouse_motion(self, pos: Tuple[int, int]):
        """Handle mouse motion for hover effects"""
        if self.state == GameState.PLAYING:
            if (GRID_OFFSET_X <= pos[0] < GRID_OFFSET_X + GRID_SIZE * CELL_SIZE and
                GRID_OFFSET_Y <= pos[1] < GRID_OFFSET_Y + GRID_SIZE * CELL_SIZE):
                col = (pos[0] - GRID_OFFSET_X) // CELL_SIZE
                row = (pos[1] - GRID_OFFSET_Y) // CELL_SIZE
                self.hovered_cell = Position(row, col)
            else:
                self.hovered_cell = None
    
    def _handle_keyboard(self, key):
        """Handle keyboard events"""
        if key == pygame.K_ESCAPE:
            if self.state == GameState.PLAYING:
                self.state = GameState.MENU
            elif self.state in [GameState.WIN, GameState.LOSE]:
                self.state = GameState.MENU
        
        # Number keys for piece selection
        if self.state == GameState.PLAYING:
            for i in range(len(self.available_pieces)):
                if self.available_pieces[i][1] > 0:
                    if key == pygame.K_1 + i:
                        self.selected_piece = self.available_pieces[i][0]
    
    def _run_simulation(self):
        """Run the vehicle simulation"""
        if not self.vehicle:
            return
        
        # Find path using BFS
        path = self._find_path()
        if path:
            self.vehicle.set_path(path)
            self.state = GameState.RUNNING
        else:
            # No valid path
            self.state = GameState.LOSE
    
    def _find_path(self) -> List[Position]:
        """Find path from start to end using BFS"""
        challenge = self.challenges[self.current_level]
        start = challenge.start_pos
        end = challenge.end_pos
        
        # BFS
        queue = [start]
        visited = {start}
        parent = {start: None}
        
        while queue:
            current = queue.pop(0)
            
            if current == end:
                # Reconstruct path
                path = []
                node = current
                while node:
                    path.append(node)
                    node = parent[node]
                return path[::-1]
            
            # Get neighbors
            neighbors = self._get_neighbors(current)
            for neighbor in neighbors:
                if neighbor not in visited and neighbor not in challenge.obstacles:
                    # Check if there's a valid connection
                    if self._can_connect(current, neighbor):
                        visited.add(neighbor)
                        parent[neighbor] = current
                        queue.append(neighbor)
        
        return []
    
    def _get_neighbors(self, pos: Position) -> List[Position]:
        """Get neighboring positions"""
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
        
        for dr, dc in directions:
            new_pos = Position(pos.row + dr, pos.col + dc)
            if new_pos.is_valid():
                neighbors.append(new_pos)
        
        return neighbors
    
    def _can_connect(self, from_pos: Position, to_pos: Position) -> bool:
        """Check if two cells can be connected"""
        if not from_pos.is_valid() or not to_pos.is_valid():
            return False
        
        from_type = self.grid[from_pos.row][from_pos.col]
        to_type = self.grid[to_pos.row][to_pos.col]
        
        # Empty cells can't connect
        if from_type == PieceType.EMPTY or to_type == PieceType.OBS:
            return False
        
        # Determine direction
        dr = to_pos.row - from_pos.row
        dc = to_pos.col - from_pos.col
        
        if dr == -1:  # to_pos is above
            direction = 'top'
            opposite = 'bottom'
        elif dr == 1:  # to_pos is below
            direction = 'bottom'
            opposite = 'top'
        elif dc == -1:  # to_pos is left
            direction = 'left'
            opposite = 'right'
        elif dc == 1:  # to_pos is right
            direction = 'right'
            opposite = 'left'
        else:
            return False
        
        from_piece = Piece.get_piece_info(from_type)
        to_piece = Piece.get_piece_info(to_type)
        
        return direction in from_piece.connections and opposite in to_piece.connections
    
    def _update(self):
        """Update game state"""
        if self.state == GameState.RUNNING and self.vehicle:
            self.vehicle.update()
            
            if not self.vehicle.is_moving:
                # Check if reached end
                challenge = self.challenges[self.current_level]
                if self.vehicle.position == challenge.end_pos:
                    self.state = GameState.WIN
                else:
                    self.state = GameState.LOSE
    
    def _draw(self):
        """Draw everything"""
        self.screen.fill(WHITE)
        
        if self.state == GameState.MENU:
            self._draw_menu()
        elif self.state in [GameState.PLAYING, GameState.RUNNING]:
            self._draw_game()
        elif self.state == GameState.WIN:
            self._draw_win()
        elif self.state == GameState.LOSE:
            self._draw_lose()
        
        pygame.display.flip()
    
    def _draw_menu(self):
        """Draw main menu"""
        # Title
        title = self.font.render("Road Builder Game", True, BLUE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = self.small_font.render("Logical Road Puzzle - Task 1 Coursework", True, GRAY)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 140))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Level buttons
        button_y = 250
        for i, challenge in enumerate(self.challenges):
            button_rect = pygame.Rect(200, button_y, 500, 50)
            pygame.draw.rect(self.screen, LIGHT_GRAY, button_rect)
            pygame.draw.rect(self.screen, DARK_GRAY, button_rect, 2)
            
            text = self.font.render(f"{i+1}. {challenge.name}", True, BLACK)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)
            
            button_y += 70
    
    def _draw_game(self):
        """Draw game screen"""
        # Draw level title
        challenge = self.challenges[self.current_level]
        title = self.font.render(challenge.name, True, BLUE)
        self.screen.blit(title, (GRID_OFFSET_X, 30))
        
        # Draw cost
        cost_text = self.small_font.render(f"Total Cost: ${self.total_cost:.2f}", True, BLACK)
        self.screen.blit(cost_text, (GRID_OFFSET_X + 300, 35))
        
        # Draw grid
        self._draw_grid()
        
        # Draw start and end markers
        start_pixel = challenge.start_pos.to_pixel()
        end_pixel = challenge.end_pos.to_pixel()
        
        pygame.draw.circle(self.screen, GREEN, start_pixel, 20)
        pygame.draw.circle(self.screen, RED, end_pixel, 20)
        
        start_label = self.small_font.render("START", True, WHITE)
        end_label = self.small_font.render("END", True, WHITE)
        self.screen.blit(start_label, (start_pixel[0] - 20, start_pixel[1] - 8))
        self.screen.blit(end_label, (end_pixel[0] - 15, end_pixel[1] - 8))
        
        # Draw vehicle
        if self.vehicle:
            vehicle_pos = self.vehicle.get_current_pixel_pos()
            pygame.draw.circle(self.screen, ORANGE, vehicle_pos, 15)
            # Draw direction indicator
            if self.vehicle.direction == 'right':
                pygame.draw.polygon(self.screen, BLACK, 
                    [(vehicle_pos[0] + 10, vehicle_pos[1]),
                     (vehicle_pos[0], vehicle_pos[1] - 5),
                     (vehicle_pos[0], vehicle_pos[1] + 5)])
            elif self.vehicle.direction == 'left':
                pygame.draw.polygon(self.screen, BLACK,
                    [(vehicle_pos[0] - 10, vehicle_pos[1]),
                     (vehicle_pos[0], vehicle_pos[1] - 5),
                     (vehicle_pos[0], vehicle_pos[1] + 5)])
            elif self.vehicle.direction == 'up':
                pygame.draw.polygon(self.screen, BLACK,
                    [(vehicle_pos[0], vehicle_pos[1] - 10),
                     (vehicle_pos[0] - 5, vehicle_pos[1]),
                     (vehicle_pos[0] + 5, vehicle_pos[1])])
            elif self.vehicle.direction == 'down':
                pygame.draw.polygon(self.screen, BLACK,
                    [(vehicle_pos[0], vehicle_pos[1] + 10),
                     (vehicle_pos[0] - 5, vehicle_pos[1]),
                     (vehicle_pos[0] + 5, vehicle_pos[1])])
        
        # Draw piece selection panel
        self._draw_piece_panel()
        
        # Draw buttons
        self._draw_buttons()
    
    def _draw_grid(self):
        """Draw the game grid"""
        challenge = self.challenges[self.current_level]
        
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = GRID_OFFSET_X + col * CELL_SIZE
                y = GRID_OFFSET_Y + row * CELL_SIZE
                
                # Draw cell background
                cell_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                
                # Check if obstacle
                if Position(row, col) in challenge.obstacles:
                    pygame.draw.rect(self.screen, DARK_GRAY, cell_rect)
                    # Draw X
                    pygame.draw.line(self.screen, RED, (x + 10, y + 10), 
                                   (x + CELL_SIZE - 10, y + CELL_SIZE - 10), 3)
                    pygame.draw.line(self.screen, RED, (x + CELL_SIZE - 10, y + 10),
                                   (x + 10, y + CELL_SIZE - 10), 3)
                else:
                    pygame.draw.rect(self.screen, LIGHT_GRAY, cell_rect)
                    pygame.draw.rect(self.screen, GRAY, cell_rect, 2)
                    
                    # Draw placed piece
                    piece_type = self.grid[row][col]
                    if piece_type != PieceType.EMPTY:
                        self._draw_piece(x, y, piece_type)
                
                # Draw hover effect
                if self.hovered_cell and self.hovered_cell == Position(row, col):
                    if piece_type == PieceType.EMPTY and self.selected_piece:
                        # Preview placement
                        preview_rect = cell_rect.copy()
                        preview_rect.inflate_ip(-4, -4)
                        pygame.draw.rect(self.screen, YELLOW, preview_rect, 3)
    
    def _draw_piece(self, x: int, y: int, piece_type: PieceType):
        """Draw a piece in the cell"""
        cx, cy = x + CELL_SIZE // 2, y + CELL_SIZE // 2
        
        if piece_type in [PieceType.ROAD_HORIZONTAL, PieceType.BRIDGE_SHORT, PieceType.BRIDGE_LONG]:
            # Horizontal road
            pygame.draw.rect(self.screen, BROWN, (x + 10, cy - 15, CELL_SIZE - 20, 30))
            pygame.draw.line(self.screen, YELLOW, (x + 10, cy), (x + CELL_SIZE - 10, cy), 2)
        
        elif piece_type in [PieceType.ROAD_VERTICAL, PieceType.RAMP_UP, PieceType.RAMP_DOWN]:
            # Vertical road
            pygame.draw.rect(self.screen, BROWN, (cx - 15, y + 10, 30, CELL_SIZE - 20))
            pygame.draw.line(self.screen, YELLOW, (cx, y + 10), (cx, y + CELL_SIZE - 10), 2)
        
        elif piece_type == PieceType.ROAD_TURN_BR:
            # Bottom to Right
            pygame.draw.rect(self.screen, BROWN, (x + 10, cy, CELL_SIZE - 10, 30))
            pygame.draw.rect(self.screen, BROWN, (cx - 15, y + 10, 30, CELL_SIZE // 2))
            pygame.draw.line(self.screen, YELLOW, (x + 10, cy), (x + CELL_SIZE - 10, cy), 2)
            pygame.draw.line(self.screen, YELLOW, (cx, cy), (cx, y + CELL_SIZE - 10), 2)
        
        elif piece_type == PieceType.ROAD_TURN_BL:
            # Bottom to Left
            pygame.draw.rect(self.screen, BROWN, (x, cy, CELL_SIZE - 10, 30))
            pygame.draw.rect(self.screen, BROWN, (cx - 15, y + 10, 30, CELL_SIZE // 2))
            pygame.draw.line(self.screen, YELLOW, (x + 10, cy), (x + CELL_SIZE - 10, cy), 2)
            pygame.draw.line(self.screen, YELLOW, (cx, cy), (cx, y + CELL_SIZE - 10), 2)
        
        elif piece_type == PieceType.ROAD_TURN_TR:
            # Top to Right
            pygame.draw.rect(self.screen, BROWN, (x + 10, cy - 15, CELL_SIZE - 10, 30))
            pygame.draw.rect(self.screen, BROWN, (cx - 15, y + 10, 30, CELL_SIZE // 2))
            pygame.draw.line(self.screen, YELLOW, (x + 10, cy), (x + CELL_SIZE - 10, cy), 2)
            pygame.draw.line(self.screen, YELLOW, (cx, y + 10), (cx, cy), 2)
        
        elif piece_type == PieceType.ROAD_TURN_TL:
            # Top to Left
            pygame.draw.rect(self.screen, BROWN, (x, cy - 15, CELL_SIZE - 10, 30))
            pygame.draw.rect(self.screen, BROWN, (cx - 15, y + 10, 30, CELL_SIZE // 2))
            pygame.draw.line(self.screen, YELLOW, (x + 10, cy), (x + CELL_SIZE - 10, cy), 2)
            pygame.draw.line(self.screen, YELLOW, (cx, y + 10), (cx, cy), 2)
    
    def _draw_piece_panel(self):
        """Draw piece selection panel on the right"""
        panel_x = GRID_OFFSET_X + GRID_SIZE * CELL_SIZE + 20
        panel_y = 100
        
        # Panel background
        panel_rect = pygame.Rect(panel_x, 50, SIDEBAR_WIDTH, SCREEN_HEIGHT - 100)
        pygame.draw.rect(self.screen, LIGHT_GRAY, panel_rect)
        
        # Title
        title = self.small_font.render("Available Pieces:", True, BLACK)
        self.screen.blit(title, (panel_x + 10, 60))
        
        # Draw piece buttons
        for i, (piece_type, count) in enumerate(self.available_pieces):
            y_pos = 100 + i * 45
            button_rect = pygame.Rect(panel_x + 10, y_pos, SIDEBAR_WIDTH - 20, 40)
            
            # Highlight selected
            if piece_type == self.selected_piece:
                pygame.draw.rect(self.screen, YELLOW, button_rect)
            else:
                pygame.draw.rect(self.screen, WHITE, button_rect)
            
            pygame.draw.rect(self.screen, GRAY, button_rect, 2)
            
            # Piece name and cost
            piece_info = Piece.get_piece_info(piece_type)
            piece_name = piece_type.name.replace('_', ' ')
            text = self.small_font.render(f"{i+1}. {piece_name} - ${piece_info.cost} (x{count})", 
                                         True, BLACK if count > 0 else GRAY)
            self.screen.blit(text, (panel_x + 20, y_pos + 10))
    
    def _draw_buttons(self):
        """Draw action buttons"""
        button_x = GRID_OFFSET_X + GRID_SIZE * CELL_SIZE + 30
        
        # Run button
        run_rect = pygame.Rect(button_x, SCREEN_HEIGHT - 150, 150, 45)
        pygame.draw.rect(self.screen, GREEN, run_rect)
        run_text = self.font.render("RUN", True, WHITE)
        run_text_rect = run_text.get_rect(center=run_rect.center)
        self.screen.blit(run_text, run_text_rect)
        
        # Reset button
        reset_rect = pygame.Rect(button_x, SCREEN_HEIGHT - 90, 150, 45)
        pygame.draw.rect(self.screen, RED, reset_rect)
        reset_text = self.font.render("RESET", True, WHITE)
        reset_text_rect = reset_text.get_rect(center=reset_rect.center)
        self.screen.blit(reset_text, reset_text_rect)
    
    def _draw_win(self):
        """Draw win screen"""
        # Background
        self.screen.fill(SKY_BLUE)
        
        # Message
        title = self.font.render("Congratulations!", True, GREEN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(title, title_rect)
        
        # Score
        challenge = self.challenges[self.current_level]
        score = self._calculate_score()
        score_text = self.font.render(f"Score: {score}/100", True, BLACK)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        cost_text = self.small_font.render(f"Total Cost: ${self.total_cost:.2f} (Par: ${challenge.par_score})", 
                                           True, BLACK)
        cost_rect = cost_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(cost_text, cost_rect)
        
        # Continue button
        continue_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 70, 150, 45)
        pygame.draw.rect(self.screen, BLUE, continue_rect)
        continue_text = self.font.render("Continue", True, WHITE)
        continue_text_rect = continue_text.get_rect(center=continue_rect.center)
        self.screen.blit(continue_text, continue_text_rect)
    
    def _draw_lose(self):
        """Draw lose screen"""
        # Background
        self.screen.fill(DARK_GRAY)
        
        # Message
        title = self.font.render("Try Again!", True, RED)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(title, title_rect)
        
        # Hint
        hint = self.small_font.render("No valid path found. Check your connections!", True, WHITE)
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
        self.screen.blit(hint, hint_rect)
        
        # Retry button
        retry_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 50, 150, 45)
        pygame.draw.rect(self.screen, ORANGE, retry_rect)
        retry_text = self.font.render("Retry", True, WHITE)
        retry_text_rect = retry_text.get_rect(center=retry_rect.center)
        self.screen.blit(retry_text, retry_text_rect)
    
    def _calculate_score(self) -> int:
        """Calculate score based on cost"""
        challenge = self.challenges[self.current_level]
        
        if self.total_cost <= challenge.par_score:
            return 100
        elif self.total_cost <= challenge.par_score * 1.5:
            return 80
        elif self.total_cost <= challenge.par_score * 2:
            return 60
        else:
            return 40


# ============================================================
# MAIN ENTRY POINT
# ============================================================

=======
                    if event.button == 1:  # Left click
                        self.handle_click(event.pos)

            # Update animation
            self.update_animation()

            # Draw
            self.draw()

            self.clock.tick(60)

        pygame.quit()
        sys.exit()


>>>>>>> f56e601d65e2c24e33985b9b1302c9416529a868
if __name__ == "__main__":
    game = RoadBuilderGame()
    game.run()

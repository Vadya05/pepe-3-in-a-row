import pygame
import random
import time

# ================= SETTINGS =================
WIDTH, HEIGHT = 600, 700
GRID_SIZE = 8          # 8x8 grid
CELL_SIZE = 60
FPS = 60

# Colors (you can replace with meme-coin themed images later)
COLORS = [
    (255, 50, 50),    # red    → $PEPE
    (50, 200, 50),    # green  → $SHIB
    (50, 50, 255),    # blue   → $SOL
    (255, 220, 0),    # yellow → $DOGE
    (200, 0, 200),    # purple → $BONK
    (255, 150, 0),    # orange → $WIF
]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pepe Match-3")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 36)

# ================= GAME LOGIC =================
grid = [[random.randint(0, len(COLORS)-1) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

score = 0
selected = None     # (row, col) or None
falling = False
game_over = False

def draw_grid():
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            color = COLORS[grid[r][c]]
            rect = pygame.Rect(c * CELL_SIZE + 60, r * CELL_SIZE + 100, CELL_SIZE - 4, CELL_SIZE - 4)
            pygame.draw.rect(screen, color, rect, border_radius=12)
            # crypto-style border
            pygame.draw.rect(screen, (255, 255, 255, 60), rect, 2, border_radius=12)

def find_matches():
    to_remove = set()

    # horizontal matches
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE - 2):
            if grid[r][c] == grid[r][c+1] == grid[r][c+2] != -1:
                to_remove.update([(r, c), (r, c+1), (r, c+2)])

    # vertical matches
    for c in range(GRID_SIZE):
        for r in range(GRID_SIZE - 2):
            if grid[r][c] == grid[r+1][c] == grid[r+2][c] != -1:
                to_remove.update([(r, c), (r+1, c), (r+2, c)])

    return to_remove

def remove_and_fall(matches):
    global score
    if not matches:
        return False

    score += len(matches) * 10

    for r, c in matches:
        grid[r][c] = -1  # mark for removal

    # fall down
    for c in range(GRID_SIZE):
        write_pos = GRID_SIZE - 1
        for r in range(GRID_SIZE - 1, -1, -1):
            if grid[r][c] != -1:
                grid[write_pos][c] = grid[r][c]
                if write_pos != r:
                    grid[r][c] = -1
                write_pos -= 1

        # fill new cells from top
        for r in range(write_pos, -1, -1):
            grid[r][c] = random.randint(0, len(COLORS) - 1)

    return True

def can_swap(r1, c1, r2, c2):
    if abs(r1 - r2) + abs(c1 - c2) != 1:
        return False
    # temporary swap
    grid[r1][c1], grid[r2][c2] = grid[r2][c2], grid[r1][c1]
    has_match = bool(find_matches())
    # revert
    grid[r1][c1], grid[r2][c2] = grid[r2][c2], grid[r1][c1]
    return has_match

# ================= MAIN LOOP =================
running = True
while running:
    dt = clock.tick(FPS)
    screen.fill((12, 14, 18))  # dark crypto background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and not falling and not game_over:
            mx, my = event.pos
            col = (mx - 60) // CELL_SIZE
            row = (my - 100) // CELL_SIZE

            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                if selected is None:
                    selected = (row, col)
                else:
                    sr, sc = selected
                    if can_swap(row, col, sr, sc):
                        # swap
                        grid[sr][sc], grid[row][col] = grid[row][col], grid[sr][sc]
                        falling = True
                    selected = None

    # process matches + falling
    if falling:
        matches = find_matches()
        if remove_and_fall(matches):
            time.sleep(0.25)  # small delay for visual effect
        else:
            falling = False

    draw_grid()

    # UI
    score_text = font.render(f"SCORE: {score}", True, (220, 220, 255))
    screen.blit(score_text, (20, 20))

    if game_over:
        go_text = font.render("GAME OVER", True, (255, 80, 80))
        screen.blit(go_text, (WIDTH // 2 - go_text.get_width() // 2, HEIGHT // 2 - 40))

    pygame.display.flip()

pygame.quit()

import random, pygame, time
import pygame.color

COLS, ROWS = 150, 80
CELL_SIZE = 10
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE
zero = None
one = not zero
BRUSH_SIZE = 3

def init_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    grid = [[zero for _ in range(COLS)] for _ in range(ROWS)]
    return screen, grid

brush_color = pygame.Color(0, 0, 0)
brush_color.hsva = (0, 80, 100, 100)
last_tick = time.time()

def update_brush_color():
    global brush_color, last_tick
    now = time.time()
    if now - last_tick > 0.5:
        h, s, v, a = brush_color.hsva
        h = (h + 10) % 360
        brush_color.hsva = (h, s ,v, a)
        last_tick = now

def handle_events(grid):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    if pygame.mouse.get_pressed()[0]:  # left button held
        mouse_pos = pygame.mouse.get_pos()
        grid_x = mouse_pos[0] // CELL_SIZE
        grid_y = mouse_pos[1] // CELL_SIZE


        update_brush_color()
        half = BRUSH_SIZE // 2
        for dy in range(-half, half+1):
            for dx in range(-half, half+1):
                ny, nx = grid_y + dy, grid_x + dx
                if 0 <= ny < ROWS and 0 <= nx < COLS:
                    grid[ny][nx] = (brush_color.r, brush_color.g, brush_color.b)
    return True


def update(grid):
    for y in range(ROWS - 2, -1, -1):
        for x in range(COLS):
            if grid[y][x] != zero:
                if grid[y + 1][x] == zero:
                    grid[y + 1][x] = grid[y][x]
                    grid[y][x] = zero
                else:
                    leftright = [-1, 1]
                    random.shuffle(leftright)
                    for dx in leftright:
                        nx = x + dx
                        if 0 <= nx < COLS and grid[y + 1][nx] is zero:
                            grid[y + 1][nx] = grid[y][x]
                            grid[y][x] = zero
                        break

def draw(screen, grid):
    screen.fill((255, 255, 255))
    for y in range(ROWS):
        for x in range(COLS):
            color = grid[y][x] if grid[y][x] is not zero else (0, 0, 0)
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)
    pygame.display.flip()



def main():
    screen, grid = init_game()
    running = True
    while running:
        running = handle_events(grid)
        update(grid)
        draw(screen, grid)


pygame.quit()

if __name__ == "__main__":
    main()
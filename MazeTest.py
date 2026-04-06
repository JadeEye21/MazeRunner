import random
import time

import pygame
import numpy as np

pygame.init()

WIDTH, HEIGHT = 1200, 800
TRANSPOSEX, TRANSPOSEY = 150, 100
BLOCK_SIZE = 20
GRIDN = 31
GRIDM = 31
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MazeRunner")
FPS = 60
FONT = pygame.font.Font('freesansbold.ttf', 14)

BGCOLOR = (102, 102, 102)
GREY = (179, 201, 201)
WHITE = (200, 200, 200)
BLACK = (1, 1, 1)
BLUE = (0, 0, 250)
RED = (250, 0, 0)
YELLOW = (247, 219, 5)
GREEN = (0, 200, 0)

WALL = 1
PATH = 0
DEAD_END = -1
START = 2
CHECKPOINT = 4
END = 9
BFS_BASE = 10
DFS_VISITED = 11

maze = np.ones((GRIDN, GRIDM), dtype=int)
checkpoints = []
FinalRoute = []
STEPS = 0


def pump_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit


def in_bounds(x, y):
    return 0 <= x < GRIDN and 0 <= y < GRIDM


def Button(x, y, w, h, message):
    pygame.draw.rect(WIN, GREY, [x, y, w, h])
    text = FONT.render(message, True, BLACK)
    WIN.blit(text, (x + 5, y + 5))


def MazeGenerator():
    frontier = [(5, 5)]
    while frontier:
        n = random.randint(0, len(frontier) - 1)
        x, y = frontier[n]

        if x + 2 < GRIDN and maze[x + 2][y] == PATH:
            maze[x + 1][y] = PATH
        elif x - 2 > 0 and maze[x - 2][y] == PATH:
            maze[x - 1][y] = PATH
        elif y + 2 < GRIDM and maze[x][y + 2] == PATH:
            maze[x][y + 1] = PATH
        elif y - 2 > 0 and maze[x][y - 2] == PATH:
            maze[x][y - 1] = PATH

        maze[x][y] = PATH

        if x + 2 < GRIDN and maze[x + 2][y] == WALL:
            frontier.append((x + 2, y))
        if x - 2 > 0 and maze[x - 2][y] == WALL:
            frontier.append((x - 2, y))
        if y + 2 < GRIDM and maze[x][y + 2] == WALL:
            frontier.append((x, y + 2))
        if y - 2 > 0 and maze[x][y - 2] == WALL:
            frontier.append((x, y - 2))

        del frontier[n]
        frontier = list(set(frontier))

    pygame.display.update()


def clearMaze():
    for x in range(GRIDN):
        for y in range(GRIDM):
            maze[x][y] = WALL


def ReRun():
    clearMaze()
    MazeGenerator()
    drawGrid()
    pygame.display.update()


def Clear():
    global STEPS
    STEPS = 0
    clearMaze()
    drawGrid()
    pygame.display.update()
    return 0


def draw_window():
    WIN.fill(BGCOLOR)
    pygame.display.update()


def drawGrid():
    for y in range(GRIDN):
        for x in range(GRIDM):
            rect = pygame.Rect(
                TRANSPOSEX + x * BLOCK_SIZE,
                TRANSPOSEY + y * BLOCK_SIZE,
                BLOCK_SIZE, BLOCK_SIZE)
            val = maze[x, y]
            if val == PATH or val == DEAD_END:
                pygame.draw.rect(WIN, WHITE, rect)
            elif val == WALL:
                pygame.draw.rect(WIN, BLACK, rect)
            elif val == START or val == BFS_BASE:
                pygame.draw.rect(WIN, BLUE, rect)
            elif val == CHECKPOINT:
                pygame.draw.rect(WIN, GREEN, rect)
            elif val == END:
                pygame.draw.rect(WIN, RED, rect)
            elif val > BFS_BASE:
                pygame.draw.rect(WIN, YELLOW, rect)
    pygame.display.flip()


def updateGrid(x, y):
    rect = pygame.Rect(
        TRANSPOSEX + x * BLOCK_SIZE,
        TRANSPOSEY + y * BLOCK_SIZE,
        BLOCK_SIZE, BLOCK_SIZE)
    val = maze[x, y]
    if val == PATH or val == DEAD_END:
        pygame.draw.rect(WIN, WHITE, rect)
    elif val == WALL:
        pygame.draw.rect(WIN, BLACK, rect)
    elif val == START or val == BFS_BASE:
        pygame.draw.rect(WIN, BLUE, rect)
    elif val == CHECKPOINT:
        pygame.draw.rect(WIN, GREEN, rect)
    elif val == END:
        pygame.draw.rect(WIN, RED, rect)
    elif val > BFS_BASE:
        pygame.draw.rect(WIN, YELLOW, rect)
    pygame.display.update(rect)


def CheckCell(x, y, posflag):
    for i in range(GRIDN):
        for j in range(GRIDM):
            x0 = TRANSPOSEX + BLOCK_SIZE * i
            y0 = TRANSPOSEY + BLOCK_SIZE * j
            if x0 <= x <= x0 + BLOCK_SIZE and y0 <= y <= y0 + BLOCK_SIZE:
                if maze[i][j] == PATH and posflag == 0:
                    maze[i][j] = START
                    drawGrid()
                    return 1
                if maze[i][j] == PATH and posflag == 1:
                    maze[i][j] = END
                    drawGrid()
                    return 2
                else:
                    return posflag
    return posflag


def ClearStartAndEnd():
    global STEPS
    for i in range(GRIDN):
        for j in range(GRIDM):
            if maze[i][j] != WALL:
                maze[i][j] = PATH
    checkpoints.clear()
    FinalRoute.clear()
    STEPS = 0
    WIN.fill(BGCOLOR, (800, 600, 100, 50))
    drawGrid()
    return 0


def find_start_end():
    init = None
    fin = None
    for i in range(GRIDN):
        for j in range(GRIDM):
            if maze[i][j] == START:
                init = (i, j)
            elif maze[i][j] == END:
                fin = (i, j)
    return init, fin


def SolveSegmentBFS(init, fin, show_path=True):
    maze[init] = BFS_BASE
    steps = BFS_BASE

    while maze[fin] in (END, PATH, CHECKPOINT):
        pump_events()
        for x in range(GRIDN):
            for y in range(GRIDM):
                if maze[x][y] == steps:
                    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        nx, ny = x + dx, y + dy
                        if in_bounds(nx, ny) and maze[nx][ny] in (PATH, END, CHECKPOINT):
                            maze[nx][ny] = steps + 1
        time.sleep(0.1)
        drawGrid()
        steps += 1

    path_cells = []
    i, j = fin
    maze[fin] = steps
    while (i, j) != init:
        pump_events()
        moved = False
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            ni, nj = i + dx, j + dy
            if in_bounds(ni, nj) and maze[ni, nj] == steps - 1:
                path_cells.append((ni, nj))
                i, j = ni, nj
                moved = True
                break
        if not moved:
            break
        steps -= 1

    for x in range(GRIDN):
        for y in range(GRIDM):
            if maze[x][y] >= BFS_BASE:
                maze[x][y] = PATH

    if show_path:
        for cell in path_cells:
            maze[cell] = START
            drawGrid()
            time.sleep(0.005)
        maze[init] = START
    else:
        for cell in path_cells:
            FinalRoute.append(cell)


def SolveUsingDFS(init, fin, show_path=True):
    global STEPS
    stack = [init]

    while stack:
        pump_events()
        maze[stack[-1]] = DFS_VISITED
        STEPS += 1
        i, j = stack[-1]

        moved = False
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            ni, nj = i + dx, j + dy
            if in_bounds(ni, nj):
                if maze[ni, nj] == PATH:
                    stack.append((ni, nj))
                    moved = True
                    break
                elif (ni, nj) == fin:
                    drawGrid()
                    _reconstruct_dfs(stack, show_path)
                    return

        if not moved:
            maze[i, j] = DEAD_END
            STEPS -= 1
            stack.pop()

        drawGrid()
        time.sleep(0.01)


def _reconstruct_dfs(stack, show_path):
    if show_path:
        while stack:
            maze[stack[-1]] = START
            stack.pop()
            drawGrid()
            time.sleep(0.005)
    else:
        while stack:
            FinalRoute.append(stack[-1])
            if stack[-1] not in checkpoints:
                maze[stack[-1]] = PATH
            stack.pop()


def AddCheckpoint(x, y):
    for i in range(GRIDN):
        for j in range(GRIDM):
            x0 = TRANSPOSEX + BLOCK_SIZE * i
            y0 = TRANSPOSEY + BLOCK_SIZE * j
            if x0 <= x <= x0 + BLOCK_SIZE and y0 <= y <= y0 + BLOCK_SIZE:
                if maze[i][j] == PATH:
                    maze[i, j] = CHECKPOINT
                    checkpoints.append((i, j))
                    drawGrid()
                    return 1
    drawGrid()
    return 0


def Routing(algorithm='dfs'):
    init, fin = find_start_end()
    if init is None or fin is None:
        print("Set start and end points first!")
        return

    maze[init] = PATH

    route_points = [init] + list(checkpoints) + [fin]
    has_checkpoints = len(route_points) > 2

    for idx in range(len(route_points) - 1):
        for x in range(GRIDN):
            for y in range(GRIDM):
                if maze[x, y] in (DEAD_END, DFS_VISITED):
                    maze[x, y] = PATH

        seg_start = route_points[idx]
        seg_end = route_points[idx + 1]

        if algorithm == 'bfs':
            SolveSegmentBFS(seg_start, seg_end,
                            show_path=not has_checkpoints)
        else:
            SolveUsingDFS(seg_start, seg_end,
                          show_path=not has_checkpoints)

    if has_checkpoints:
        while FinalRoute:
            cell = FinalRoute.pop()
            if cell in checkpoints:
                maze[cell] = CHECKPOINT
            else:
                maze[cell] = START
            drawGrid()
            time.sleep(0.005)

    maze[init] = START
    maze[fin] = END
    drawGrid()


def main():
    global STEPS
    posflag = 0
    checkflag = 0
    clock = pygame.time.Clock()
    run = True
    draw_window()
    MazeGenerator()
    drawGrid()

    btn_gen = pygame.Rect(50, 30, 100, 50)
    btn_clear = pygame.Rect(200, 30, 100, 50)
    btn_restart = pygame.Rect(350, 30, 100, 50)
    btn_bfs = pygame.Rect(500, 30, 100, 50)
    btn_dfs = pygame.Rect(650, 30, 100, 50)
    btn_checkpoint = pygame.Rect(800, 30, 120, 50)

    Button(btn_gen.x, btn_gen.y, btn_gen.w, btn_gen.h, 'Generate')
    Button(btn_clear.x, btn_clear.y, btn_clear.w, btn_clear.h, 'Clear')
    Button(btn_restart.x, btn_restart.y, btn_restart.w, btn_restart.h, 'Restart')
    Button(btn_bfs.x, btn_bfs.y, btn_bfs.w, btn_bfs.h, 'Solve by BFS')
    Button(btn_dfs.x, btn_dfs.y, btn_dfs.w, btn_dfs.h, 'Solve by DFS')
    Button(btn_checkpoint.x, btn_checkpoint.y, btn_checkpoint.w, btn_checkpoint.h, 'Add checkpoint')

    text = FONT.render(str(STEPS), True, BLACK)
    WIN.blit(text, (800, 600))
    pygame.display.update()

    while run:
        clock.tick(FPS // 10)
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_gen.collidepoint(mouse):
                    posflag = 0
                    checkpoints.clear()
                    FinalRoute.clear()
                    ReRun()

                elif btn_clear.collidepoint(mouse):
                    posflag = Clear()
                    checkpoints.clear()
                    FinalRoute.clear()

                elif btn_restart.collidepoint(mouse):
                    posflag = ClearStartAndEnd()

                elif btn_checkpoint.collidepoint(mouse) and posflag == 2:
                    checkflag += 1

                elif btn_bfs.collidepoint(mouse) and posflag == 2:
                    WIN.fill(BGCOLOR, (800, 600, 100, 50))
                    FinalRoute.clear()
                    STEPS = 0
                    Routing('bfs')
                    drawGrid()
                    text = FONT.render(str(STEPS), True, BLACK)
                    WIN.blit(text, (800, 600))
                    pygame.display.flip()
                    posflag = 0

                elif btn_dfs.collidepoint(mouse) and posflag == 2:
                    WIN.fill(BGCOLOR, (800, 600, 100, 50))
                    FinalRoute.clear()
                    STEPS = 0
                    Routing('dfs')
                    drawGrid()
                    text = FONT.render(str(STEPS), True, BLACK)
                    WIN.blit(text, (800, 600))
                    pygame.display.flip()
                    posflag = 0

                elif posflag < 2:
                    posflag = CheckCell(mouse[0], mouse[1], posflag)

                elif checkflag == 1:
                    AddCheckpoint(mouse[0], mouse[1])
                    checkflag -= 1

    pygame.quit()


if __name__ == '__main__':
    main()

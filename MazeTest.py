import random
import time

import pygame
import numpy as np
import os

pygame.init()

WIDTH, HEIGHT = 1200, 800
TRANSPOSEX, TRANSPOSEY = 180,100
blockSize = 20
GRIDN=31
GRIDM=31
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MazeRunner")
FPS = 60
FONT = pygame.font.Font('freesansbold.ttf', 14)
BGCOLOR = (102, 102, 102)
GREY = (179, 201, 201)
WHITE = (200,200,200)
BLACK = (1,1,1)
BLUE = (0, 0, 250)
RED = (250, 0, 0)
YELLOW = (247, 219, 5)


# maze = np.zeros((GRIDM, GRIDN))
maze = np.ones((GRIDN, GRIDM))
# maze = np.random.randint( 2, size=(GRIDN, GRIDM))

def Button(x, y, buttonSizeX, buttonSizeY, message):
    pygame.draw.rect(WIN, GREY,[x, y, buttonSizeX, buttonSizeY])
    text = FONT.render(message, True, BLACK)
    WIN.blit(text, (x+5, y+5))


def AlternateBlack():
    for x in range(0,GRIDN, 2):
        for y in range(0, GRIDM, 2):
            maze[x][y]=1


def MazeGenerator():
    print("Generating Maze")
    next = []
    next.append([5,5])
    run = True
    t=3
    while run:
        si = len(next)
        n = random.randint(0, si-1)
        x = next[n][0]
        y = next[n][1]
        if x + 2 < GRIDN and maze[x + 2][y] == 0:
            maze[x+1][y] = 0
        elif x - 2 > 0 and maze[x - 2][y] == 0:
            maze[x-1][y] = 0
        elif y + 2 < GRIDM and maze[x][y + 2] == 0:
            maze[x][y+1] = 0
        elif y - 2 > 0 and maze[x][y - 2] == 0:
            maze[x][y-1] = 0

        maze[x][y] = 0
        # print(len(next))
        # print((x, y))
        if x+2 < GRIDN and maze[x+2][y] ==1:
            next.append((x+2, y))

            # print(1)
        if x-2 >0 and maze[x-2][y] ==1:

            next.append((x-2, y))
            # print(2)
        if y+2 < GRIDM and maze[x][y+2] ==1:

            next.append((x, y+2))
            # print(3)
        if y-2 >0 and maze[x][y-2] ==1:

            next.append((x, y-2))
            # print(4)
        del next[n]
        next = list(set(next))
        t-=1
        # len(next) == 0
        if len(next) == 0:
            run= False
    pygame.display.update()


def ReRun():
    print("ReRunning")
    clearMaze()
    MazeGenerator()
    drawGrid()
    pygame.display.update()


def Clear():
    POSFLAG=0
    print("Clearing")
    clearMaze()
    drawGrid()
    pygame.display.update()


def clearMaze():

    for x in range(GRIDN):
        for y in range(GRIDM):
            maze[x][y]=1


def draw_window():
    WIN.fill(BGCOLOR)

    pygame.display.update()


def drawGrid():
    # blockSize = 20  #Set the size of the grid block
    for y in range(GRIDN):
        for x in range(GRIDM):
            rect = pygame.Rect(
                TRANSPOSEX+x*(blockSize),
                TRANSPOSEY+y*(blockSize),
                blockSize, blockSize)
            if maze[x,y]==0 :
                pygame.draw.rect(WIN, WHITE, rect)
            elif maze[x,y] == 1:
                pygame.draw.rect(WIN, BLACK, rect)
            elif maze[x, y] == 2 or maze[x,y] == 10:
                pygame.draw.rect(WIN, BLUE, rect)
            elif maze[x, y] == 9:
                pygame.draw.rect(WIN, RED, rect)
            elif maze[x,y] >10:
                pygame.draw.rect(WIN, YELLOW, rect)

    pygame.display.update()


def CheckCell(x, y, POSFLAG):
    for i in range(GRIDN - 1):
        for j in range(GRIDM - 1):
            if TRANSPOSEX+blockSize*i <= x <= TRANSPOSEX+blockSize*(i+1) and TRANSPOSEY+blockSize*j <= y <= TRANSPOSEY+blockSize*(j+1):
                if maze[i][j] == 0 and POSFLAG == 0:
                    maze[i][j] = 2
                    drawGrid()
                    return 1
                    # print(POSFLAG)
                if maze[i][j] == 0 and POSFLAG == 1:
                    maze[i][j] = 9
                    drawGrid()
                    return 2
                    # print(POSFLAG)
                else:
                    print("wrong click")
                    return POSFLAG
    return 0

def ClearStartAndEnd():
    for i in range(GRIDN-1):
        for j in range(GRIDM-1):
            if maze[i][j] >1:
                maze[i][j]=0
    drawGrid()
    return 0

def PrintMaze():
    for i in range(GRIDN-1):
        for j in range(GRIDM-1):
            print(maze[i][j], end=' ')
        print()


def Solve():
    init = ()
    fin = ()
    for i in range(GRIDN-1):
        for j in range(GRIDM-1):
            if maze[i][j] == 2:
                init = (i, j)
                maze[i][j] = 0
            elif maze[i][j] == 9:
                fin = (i, j)

    steps = 10
    maze[init[0]][init[1]] = steps
    while maze[fin[0]][fin[1]] ==9:
        for x in range(GRIDN):
            for y in range(GRIDM):
                if maze[x][y] == steps:
                    if maze[x+1][y] == 0 or maze[x+1][y] ==9:
                        maze[x+1][y] = steps+1
                    if maze[x-1][y] == 0 or maze[x-1][y] == 9:
                        maze[x-1][y] = steps + 1
                    if maze[x][y+1] == 0 or maze[x][y+1]==9:
                        maze[x][y+1] = steps + 1
                    if maze[x][y-1] == 0 or maze[x][y-1] ==9:
                        maze[x][y-1] = steps + 1
        time.sleep(0.1)
        drawGrid()
        steps+=1
    i, j = fin
    maze[fin] = 9
    while maze[init] != 2:
        if maze[i+1, j] == steps-1:
            maze[i+1,j] = 2
            i+=1
        elif maze[i-1, j] == steps-1:
            maze[i-1,j] = 2
            i-=1
        elif maze[i, j+1] == steps-1:
            maze[i,j+1] = 2
            j+=1
        elif maze[i, j-1] == steps-1:
            maze[i,j-1] = 2
            j-=1
        steps -= 1
        drawGrid()
        time.sleep(0.05)
    PrintMaze()


def main():

    POSFLAG = 0
    print(type(POSFLAG))
    clock = pygame.time.Clock()
    run = True
    draw_window()
    MazeGenerator()
    drawGrid()
    button_location_x = 50
    button_location_y = 30
    Button(button_location_x, button_location_y, 100, 50, 'Generate')
    Button(200, 30, 100, 50, 'Clear')
    Button(350, 30, 100, 50, 'Restart')
    Button(500, 30, 100, 50, 'Solve')

    pygame.display.update()
    while run:
        clock.tick(FPS//10)
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Exiting...")
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_location_x <= mouse[0]<=button_location_x+100 and button_location_y <= mouse[1] <= button_location_y+50:
                    POSFLAG = 0
                    ReRun()
                elif 200 <= mouse[0] <= 200+100 and button_location_y <= mouse[1] <= button_location_y+50:
                    Clear()
                elif 350 <= mouse[0] <=350+100 and button_location_y <= mouse[1] <= button_location_y+50:
                    POSFLAG = ClearStartAndEnd()
                    print(POSFLAG)
                elif 500 <= mouse[0] <= 500+100 and button_location_y <= mouse[1] <= button_location_y+50 and POSFLAG == 2:
                    print('Solving...')
                    Solve()
                    drawGrid()
                elif POSFLAG < 2:
                    POSFLAG = CheckCell(mouse[0], mouse[1], POSFLAG)
                    print(POSFLAG)


    pygame.quit()
    print("main window")


if __name__ == '__main__':

    main()


import random

import pygame
import numpy as np
import os

pygame.init()

WIDTH, HEIGHT = 1200, 800
TRANSPOSEX, TRANSPOSEY = 180,100

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
    blockSize = 20  #Set the size of the grid block
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
    pygame.display.update()


def main():

    clock = pygame.time.Clock()
    run = True
    draw_window()
    MazeGenerator()
    drawGrid()
    button_location_x = 50
    button_location_y = 30
    Button(button_location_x, button_location_y, 100, 50, 'ReRun')
    Button(200, 30, 100, 50, 'Clear')
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
                    ReRun()
                elif 200 <= mouse[0] <= 200+100 and button_location_y <= mouse[1] <= button_location_y+50:
                    Clear()

    pygame.quit()
    print("main window")


if __name__ == '__main__':

    main()


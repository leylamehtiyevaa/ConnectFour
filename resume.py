import sys
import math
import os
from button import Button
import pygame
import numpy as np


ROW_COUNT = 9
COLUMN_COUNT = 9

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

SQUARESIZE = 100
width = (COLUMN_COUNT + 2) * SQUARESIZE
height = ROW_COUNT * SQUARESIZE
size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)
screen = pygame.display.set_mode(size)


def createBoard():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def dropPiece(board, row, col, piece):
    row = int(row)  # Convert row to integer
    col = int(col)  # Convert col to integer
    board[row][col] = piece


def printBoard(board):
    print(np.flip(board, 0))


def isValidLocation(board, col):
   return col >= 0 and col < len(board[ROW_COUNT - 1]) and board[ROW_COUNT - 1][col] == 0


def getNextOpenRow(board, col):
   for r in range(ROW_COUNT):
       if 0 <= col < len(board[ROW_COUNT - 1]):
         if board[r][col] == 0:
            return r


def winningMove(board, piece):
   #Checking Horizontally
   for i in range(COLUMN_COUNT-3):
      for j in range(ROW_COUNT):
         if board[j][i] == piece and board[j][i+1] == piece and board[j][i+2] == piece and board[j][i+3] == piece:
             return True

   # Checking Vertically
   for i in range(COLUMN_COUNT):
      for j in range(ROW_COUNT-3):
         if board[j][i] == piece and board[j+1][i] == piece and board[j+2][i] == piece and board[j+3][i] == piece:
             return True

   # Checking positively sloped diaganols
   for i in range(COLUMN_COUNT-3):
      for j in range(ROW_COUNT-3):
         if board[j][i] == piece and board[j+1][i+1] == piece and board[j+2][i+2] == piece and board[j+3][i+3] == piece:
             return True

   # Check negatively sloped diaganols
   for i in range(COLUMN_COUNT-3):
      for j in range(3, ROW_COUNT):
         if board[j][i] == piece and board[j-1][i+1] == piece and board[j-2][i+2] == piece and board[j-3][i+3] == piece:
             return True


def drawBoard(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    pygame.display.update()

def devam():
    turn = 0
    def oyunDevam(board):
        word = "Free Slot"
        word1 = "Red is Played"
        word2 = "Yellow is Played"

        with open("Tahta.txt", "r") as file1:
            for line in file1:
                if len(line) >= 5:
                    first_char = line[1]
                    second_char = line[4]

                    if word in line:
                        piece = 0
                    elif word1 in line:
                        piece = 1
                    elif word2 in line:
                        piece = 2

                    dropPiece(board, int(first_char), int(second_char), piece)




    pygame.init()

    board = createBoard()
    oyunDevam(board)

    myfont = pygame.font.SysFont("monospace", 20)

    def quitGame():
        pygame.quit()
        quit()


    # Create the buttons
    buttonQuit = Button("Quit", (950, 700), (100, 50), (255, 0, 0), (0, 255, 0), (255, 255, 255), quitGame)

    buttonQuit.draw(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] >= 0 and mouse_pos[0] < width - (2 * SQUARESIZE) and mouse_pos[1] >= 0 and mouse_pos[
                    1] < height:
                    posx = mouse_pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if turn == 0:
                        turn = 1

                        if isValidLocation(board, col):
                            row = getNextOpenRow(board, col)
                            dropPiece(board, row, col, 1)

                        if winningMove(board, 1):
                            label = myfont.render("Player 1 Wins!", 1, RED)
                            screen.blit(label, (910, 10))
                            running = False


                    elif turn == 1:
                        turn = 0

                        if isValidLocation(board, col):
                            row = getNextOpenRow(board, col)
                            dropPiece(board, row, col, 2)

                        if winningMove(board, 2):
                            label = myfont.render("Player 2 Wins!", 1, YELLOW)
                            screen.blit(label, (910, 10))
                            running = False

            drawBoard(board)

    pygame.quit()
    pygame.time.wait(1000)


devam()



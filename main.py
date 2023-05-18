import sys
import numpy as np
import pygame
import math
import os

from button import Button


ROW_COUNT = 9
COLUMN_COUNT = 9

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

SQUARESIZE = 100
width = (COLUMN_COUNT + 2) * SQUARESIZE
height = ROW_COUNT * SQUARESIZE
size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)


def createBoard():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def dropPiece(board, row, col, piece):
   board[row][col] = piece


def printBoard(board):
    print(np.flip(board, 0))


file = open("Hamle.txt", "w")
file1 = open("Tahta.txt", "w")


def allPositions(board, row, col, piece):
   numRows, numCols = board.shape
   with open("Tahta.txt", "w") as file1:
       for row in range(numRows):
           for col in range(numCols):
               if  board[row][col] == 1:
                   file1.write(f"({row}, {col}) - Red is Played \n")
               elif  board[row][col] == 2:
                   file1.write(f"({row}, {col}) - Yellow is Played\n")
               else:
                 file1.write(f"({row}, {col}) - Free Slot \n")

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
         pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE, SQUARESIZE, SQUARESIZE))
         pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)

      for c in range(COLUMN_COUNT):
         for r in range(ROW_COUNT):
            if board[r][c] == 1:
                  pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
               pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2),height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
   pygame.display.update()

def Game():
    board = createBoard()
    game_over = False
    turn = 0

    screen = pygame.display.set_mode(size)
    drawBoard(board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 20)

    clock = pygame.time.Clock()
    def quitGame():
        pygame.quit()
        quit()


    # Create the buttons
    buttonQuit = Button("Quit", (950, 700), (100, 50), (255, 0, 0), (0, 255, 0), (255, 255, 255), quitGame)



    buttonQuit.draw(screen)
    pygame.display.update()

    while not game_over:

       for event in pygame.event.get():
          if event.type == pygame.QUIT:
             sys.exit()
          buttonQuit.handle_event(event)
          clock.tick(60)


          if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] >= 0 and mouse_pos[0] < width - (2 * SQUARESIZE) and mouse_pos[1] >= 0 and mouse_pos[1] < height:
             pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))


              #Ask for Player 1 Input
             if turn == 0:
                posx = event.pos[0]
                posy = event.pos[1]
                col = int(math.floor(posx/SQUARESIZE))

                coordinates = event.pos
                position = tuple((value // 100) for value in coordinates)
                satir = position[0] + 1
                sutun = 9 - position[1]
                print(satir, sutun)
                s1 = file.write(str(satir))
                s2 = file.write(str(sutun) + "\n")


                turn = 1

                if isValidLocation(board, col):
                   row = getNextOpenRow(board, col)
                   dropPiece(board,  row, col, 1)


                   if winningMove(board, 1):
                      label = myfont.render("Player 1 Wins!", 1, RED)
                      screen.blit(label, (910, 10))
                      game_over = True


             # Ask for Player 2 Input
             elif turn == 1:
               posx = event.pos[0]
               col = int(math.floor(posx / SQUARESIZE))

               coordinates = event.pos
               position = tuple((value // 100) for value in coordinates)
               satir = position[0]
               sutun = 8 - position[1]
               print(satir, sutun)
               s1 = file.write(str(satir))
               s2 = file.write(str(sutun) + "\n")

               turn = 0

               if isValidLocation(board, col):
                  row = getNextOpenRow(board, col)
                  dropPiece(board, row, col, 2)


               if winningMove(board, 2):
                  label = myfont.render("Player 2 Wins!", 1, YELLOW)
                  screen.blit(label, (910, 10))
                  game_over = True


             printBoard(board)
             drawBoard(board)
             allPositions(board, row, col, position)

             if game_over:
                pygame.time.wait(1000)
                pygame.quit()
                file.close()


pygame.init()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Menu")
pygame.draw.circle(screen, YELLOW, (200, 400), RADIUS)
pygame.draw.circle(screen, RED, (100, 500), RADIUS)
pygame.draw.circle(screen, YELLOW, (300, 640), RADIUS)
pygame.draw.circle(screen, RED, (900, 850), RADIUS)
pygame.draw.circle(screen, BLUE, (600, 100), RADIUS)
pygame.draw.circle(screen, RED, (790, 700), RADIUS)
pygame.draw.circle(screen, BLUE, (990, 900), RADIUS)
pygame.draw.circle(screen, BLUE, (650, 750), RADIUS)
pygame.draw.circle(screen, YELLOW, (650, 200), RADIUS)
pygame.draw.circle(screen, BLUE, (880, 170), RADIUS)



def startGame():
    Game()

def resumedGame():
    pass

def quitGameMenu():
    pygame.quit()
    quit()

buttonStart = Button("Start New Game", (450, 500), (200, 50), (255, 0, 0), (0, 255, 0), (255, 255, 255), startGame)
buttonResume = Button("Resume The Game", (450, 600), (200, 50), (255, 0, 0), (0, 255, 0), (255, 255, 255), resumedGame)
buttonQuitMenu = Button("Quit The Game", (450, 700), (200, 50), (255, 0, 0), (0, 255, 0), (255, 255, 255), quitGameMenu)


pygame.init()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if buttonResume.handle_event(event):
                    resumedGame()

            buttonStart.handle_event(event)
            buttonQuitMenu.handle_event(event)

    buttonStart.draw(screen)
    buttonResume.draw(screen)
    buttonQuitMenu.draw(screen)

    pygame.display.update()





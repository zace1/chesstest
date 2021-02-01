# main stores all info about current state

import pygame as p
from engine1 import *

p.init()
Width = 512
Height = Width
NumOfRowsAndColumns = 8
SizeOfSquare = Width//NumOfRowsAndColumns
PieceScale = 1
PieceDimensions = int(SizeOfSquare*PieceScale)
fps = 15
images = {}


def loadImages():
    pieces = ['wp', 'wB', 'wK', 'wN', 'wQ', 'wR',
              'bp', 'bB', 'bK', 'bN', 'bQ', 'bR']
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("piece_images_1/" + piece + ".png"), (PieceDimensions, PieceDimensions))


def drawBoard(screen):
    for i in range(NumOfRowsAndColumns):
        for j in range(NumOfRowsAndColumns):
            if i % 2 == 0:
                if j % 2 == 0:
                    color = p.Color('white')
                else:
                    color = p.Color('dark grey')
            else:
                if j % 2 == 0:
                    color = p.Color('dark grey')
                else:
                    color = p.Color('white')
            p.draw.rect(screen, color, p.Rect(i*SizeOfSquare, j*SizeOfSquare, SizeOfSquare, SizeOfSquare))


def drawPieces(screen, board):
    for i in range(NumOfRowsAndColumns):
        for j in range(NumOfRowsAndColumns):
            piece = board[j][i]
            if piece != '00':
                screen.blit(images[piece], p.Rect(i*SizeOfSquare, j*SizeOfSquare, PieceDimensions, PieceDimensions))


def main():
    screen = p.display.set_mode((Width, Height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = GameState()
    loadImages()
    running = True
    while running:
        for i in p.event.get():
            if i.type == p.QUIT:
                running = False
        drawGameStates(screen, gs)
        clock.tick(fps)
        p.display.flip()


def drawGameStates(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


if __name__ == "__main__":
    main()




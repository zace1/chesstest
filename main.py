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


def load_images():
    pieces = ['wp', 'wB', 'wK', 'wN', 'wQ', 'wR',
              'bp', 'bB', 'bK', 'bN', 'bQ', 'bR']
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("piece_images_1/" + piece + ".png"),
                                          (PieceDimensions, PieceDimensions))


def draw_board(screen):
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


def draw_pieces(screen, board):
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
    load_images()
    running = True
    initial_square = ()
    player_clicks = []       # contains two tuples in a list
    while running:
        for i in p.event.get():
            if i.type == p.QUIT:
                running = False
            elif i.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                row = location[1] // SizeOfSquare
                col = location[0] // SizeOfSquare         # location[0] = x location[1] = y
                if initial_square == (row, col):
                    initial_square = ()
                    player_clicks = []
                else:
                    initial_square = (row, col)
                    player_clicks.append(initial_square)
                if len(player_clicks) == 2:
                    move = Move(player_clicks[0], player_clicks[1], gs.board)
                    piece_moved = gs.board[player_clicks[0][0]][player_clicks[0][1]]
                    if gs.board[player_clicks[1][0]][player_clicks[1][1]] != '00':
                        capture = True
                    else:
                        capture = False
                    print(move.get_notation(piece_moved, capture))
                    gs.make_move(move)
                    initial_square = ()
                    player_clicks = []
        draw_game_states(screen, gs)
        clock.tick(fps)
        p.display.flip()


def draw_game_states(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)


if __name__ == "__main__":
    main()

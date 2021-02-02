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
    moves_raw = []
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
                    piece_moved = gs.board[player_clicks[0][0]][player_clicks[0][1]]
                    first_click = Move(player_clicks[0], False, piece_moved, gs.board)      # horrible solution to allow access to check_for_legality()
                    if len(player_clicks) == 1:
                        possible_moves = first_click.get_all_possible_moves(player_clicks[0], piece_moved, gs.board)
                        possible_moves_visual = possible_moves[0]
                        moves_raw = possible_moves[1]
                        print('legal moves:\n')
                        print(possible_moves_visual)
                if len(player_clicks) == 2:
                    piece_moved = gs.board[player_clicks[0][0]][player_clicks[0][1]]
                    if piece_moved != '00':
                        move = Move(player_clicks[0], player_clicks[1], piece_moved, gs.board)
                        if gs.board[player_clicks[1][0]][player_clicks[1][1]] != '00':
                            capture = True
                        else:
                            capture = False
                        notated_move = move.get_notation(capture, gs.board)
                        if (move.endRow, move.endCol) in moves_raw:
                            gs.make_move(move, piece_moved)
                            print('move played:\n')
                            print(notated_move)
                        else:
                            print('not legal\n')
                        moves_raw = []
                        initial_square = ()
                        player_clicks = []
                    else:
                        initial_square = ()
                        player_clicks = []
        draw_game_states(screen, gs)
        if moves_raw and len(player_clicks) == 1:
            for squares in moves_raw:
                p.draw.circle(screen, (0, 135, 0),
                              (((Width / NumOfRowsAndColumns) * int(squares[1]) + ((Width / NumOfRowsAndColumns) / 2)),
                                ((Width / NumOfRowsAndColumns) * int(squares[0]) + ((Width / NumOfRowsAndColumns) / 2))), 5)
        clock.tick(fps)
        p.display.flip()


def draw_game_states(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)


if __name__ == "__main__":
    main()

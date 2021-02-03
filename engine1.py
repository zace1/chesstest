from main import *

class GameState():
    def __init__(self):
        # "00" empty space
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["00", "00", "00", "00", "00", "00", "00", "00"],
            ["00", "00", "00", "00", "00", "00", "00", "00"],
            ["00", "00", "00", "00", "00", "00", "00", "00"],
            ["00", "00", "00", "00", "00", "00", "00", "00"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToPlay = True
        self.moveLog = []
        self.AbleToCastle = True

    def make_move(self, move, piece_moved):
        self.board[move.startRow][move.startCol] = "00"
        self.board[move.endRow][move.endCol] = piece_moved
        self.moveLog.append(move)
        self.whiteToPlay = not self.whiteToPlay


class Move:
    # set notation
    rows = {"1": 7, "2": 6, "3": 5, "4": 4,
            "5": 3, "6": 2, "7": 1, "8": 0}
    ranks = {v: k for k, v in rows.items()}         # 7: '1', 6: '2'...
    cols = {"a": 0, "b": 1, "c": 2, "d": 3,
            "e": 4, "f": 5, "g": 6, "h": 7}
    files = {v: k for k, v in cols.items()}         # 0: 'a', 1: 'b'...

    def __init__(self, start_square, end_square, piece_type, board):
        self.startRow = start_square[0]
        self.startCol = start_square[1]
        if end_square is not False:
            self.endRow = end_square[0]
            self.endCol = end_square[1]
            self.pieceCaptured = board[self.endRow][self.endCol]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.piece_type = piece_type

    def check_for_other_of_same_piece(self, capture, board, white_to_play, endswith):
        other_piece_moves = []
        initial = endswith
        specify = 0
        for i in range(NumOfRowsAndColumns):
            for j in range(NumOfRowsAndColumns):
                if board[i][j] == self.pieceMoved and (i, j) != (self.startRow, self.startCol):
                    other_piece = Move((i, j), (self.endRow, self.endCol), 'wN', board)
                    other_piece_moves = other_piece.get_all_possible_moves((i, j), board, white_to_play, True)
                    if other_piece_moves:
                        for k in other_piece_moves:
                            if k == (self.endRow, self.endCol):
                                if other_piece.startCol == self.startCol:
                                    specify = 2  # specify Rank
                                else:
                                    specify = 1  # specify File
        if specify == 2:
            initial = endswith + self.ranks[self.startRow]
        elif specify == 1:
            initial = endswith + self.files[self.startCol]
        if capture is False:
            return initial + self.get_file_rank(self.endRow, self.endCol)
        else:
            return initial + 'x' + self.get_file_rank(self.endRow, self.endCol)

    def get_notation(self, capture, board, white_to_play, promote=False):
        if self.pieceMoved.endswith('p'):
            if promote is True:
                pass
            if capture is False:
                return self.get_file_rank(self.endRow, self.endCol)
            else:
                return self.files[self.startCol] + 'x' + self.get_file_rank(self.endRow, self.endCol)
        if self.pieceMoved.endswith('B'):
            endswith = 'B'
            return self.check_for_other_of_same_piece(capture, board, white_to_play, endswith)
        if self.pieceMoved.endswith('N'):
            endswith = 'N'
            return self.check_for_other_of_same_piece(capture, board, white_to_play, endswith)
        if self.pieceMoved.endswith('R'):
            endswith = 'R'
            return self.check_for_other_of_same_piece(capture, board, white_to_play, endswith)
        if self.pieceMoved.endswith('Q'):
            endswith = 'Q'
            return self.check_for_other_of_same_piece(capture, board, white_to_play, endswith)
        return self.pieceMoved + self.get_file_rank(self.startRow, self.startCol) + \
            self.get_file_rank(self.endRow, self.endCol)

    def get_file_rank(self, row, col):
        return self.files[col] + self.ranks[row]

    def check_for_legality(self, legal_moves):
        iterable = 0
        for i in legal_moves:
            legal_moves[iterable] = self.get_file_rank(i[0], i[1])
            iterable += 1
        return legal_moves

    @staticmethod
    def check_for_legality_with_capture_list(legal_moves, piece, capture_list, start, board, white_to_play):
        formatted_legal_moves = list(legal_moves)
        for i in range(len(legal_moves)):
            potential_move = Move(start, (int(legal_moves[i][0]), int(legal_moves[i][1])), piece, board)
            capture = False
            for j in range(len(capture_list)):
                if legal_moves[i] == capture_list[j]:
                    capture = True
            formatted_legal_moves[i] = (potential_move.get_notation(capture, board, white_to_play))
        return formatted_legal_moves

    def same_side(self, change_y, change_x, side, board):
        if board[self.startRow + change_y][self.startCol + change_x].startswith(side) is True:
            return True
        return False

    def get_all_possible_moves(self, start, board, white_to_play, knight_check=False):
        if self.pieceMoved.startswith('w'):
            side = 'w'
        else:
            side = 'b'
        if (side == 'w' and white_to_play is True) or (side == 'b' and white_to_play is False):  # parentheses for visualization
            possible_moves = []
            possible_captures = []
            if self.pieceMoved == 'wp':     # white pawn
                if board[self.startRow-1][self.startCol] == '00':
                    possible_moves.append((self.startRow - 1, self.startCol))
                    if self.startRow == 6 and board[4][self.startCol] == '00':
                        possible_moves.append((4, self.startCol))
                if self.startCol != 7:
                    if board[self.startRow - 1][self.startCol + 1] != '00' and self.same_side(-1, 1, 'w', board) is False:
                        possible_moves.append((self.startRow - 1, self.startCol+1))
                if self.startCol != 0:
                    if board[self.startRow - 1][self.startCol - 1] != '00' and self.same_side(-1, -1, 'w', board) is False:
                        possible_moves.append((self.startRow - 1, self.startCol - 1))
            if self.pieceMoved == 'bp':     # black pawn
                if board[self.startRow+1][self.startCol] == '00':
                    possible_moves.append((self.startRow + 1, self.startCol))
                    if self.startRow == 1 and board[3][self.startCol] == '00':
                        possible_moves.append((3, self.startCol))
                if self.startCol != 7:
                    if board[self.startRow + 1][self.startCol + 1] != '00' and self.same_side(1, 1, 'b', board) is False:
                        possible_moves.append((self.startRow+1, self.startCol+1))
                if self.startCol != 0:
                    if board[self.startRow + 1][self.startCol - 1] != '00'and self.same_side(1, -1, 'b', board) is False:
                        possible_moves.append((self.startRow + 1, self.startCol - 1))
            if self.pieceMoved == 'wN' or self.pieceMoved == 'bN':      # knight
                if self.startRow > 0:
                    if self.startCol > 1 and self.same_side(-1, -2, side, board) is False:
                        possible_moves.append((self.startRow - 1, self.startCol - 2))
                    if self.startCol < 6 and self.same_side(-1, 2, side, board) is False:
                        possible_moves.append((self.startRow - 1, self.startCol + 2))
                    if self.startRow > 1:
                        if self.startCol > 0 and self.same_side(-2, -1, side, board) is False:
                            possible_moves.append((self.startRow - 2, self.startCol - 1))
                        if self.startCol < 7 and self.same_side(-2, 1, side, board) is False:
                            possible_moves.append((self.startRow - 2, self.startCol + 1))
                if self.startRow < 7:
                    if self.startCol > 1 and self.same_side(1, -2, side, board) is False:
                        possible_moves.append((self.startRow + 1, self.startCol - 2))
                    if self.startCol < 6 and self.same_side(1, 2, side, board) is False:
                        possible_moves.append((self.startRow + 1, self.startCol + 2))
                    if self.startRow < 6:
                        if self.startCol > 0 and self.same_side(2, -1, side, board) is False:
                            possible_moves.append((self.startRow + 2, self.startCol - 1))
                        if self.startCol < 7 and self.same_side(2, 1, side, board) is False:
                            possible_moves.append((self.startRow + 2, self.startCol + 1))
            if self.pieceMoved == 'wB' or self.pieceMoved == 'bB' or self.pieceMoved == 'wQ' or self.pieceMoved == 'bQ':      # bishop
                num_moves = 1
                temp_count = (min(self.startRow, self.startCol))     # up left
                while num_moves <= temp_count >= 0:
                    if board[self.startRow-num_moves][self.startCol-num_moves] == '00':
                        possible_moves.append((self.startRow-num_moves, self.startCol-num_moves))
                        num_moves += 1
                    elif self.same_side(-num_moves, -num_moves, side, board) is True:
                        temp_count = 0
                    else:
                        possible_moves.append((self.startRow-num_moves, self.startCol-num_moves))
                        temp_count = 0
                temp_count = (min(self.startRow, 7-self.startCol))      # up right
                num_moves = 1
                while num_moves <= temp_count >= 0:
                    if board[self.startRow-num_moves][self.startCol+num_moves] == '00':
                        possible_moves.append((self.startRow-num_moves, self.startCol+num_moves))
                        num_moves += 1
                    elif self.same_side(-num_moves, num_moves, side, board) is True:
                        temp_count = 0
                    else:
                        possible_moves.append((self.startRow-num_moves, self.startCol+num_moves))
                        temp_count = 0
                temp_count = (min(7-self.startRow, self.startCol))      # down left
                num_moves = 1
                while num_moves <= temp_count >= 0:
                    if board[self.startRow+num_moves][self.startCol-num_moves] == '00':
                        possible_moves.append((self.startRow+num_moves, self.startCol-num_moves))
                        num_moves += 1
                    elif self.same_side(num_moves, -num_moves, side, board) is True:
                        temp_count = 0
                    else:
                        possible_moves.append((self.startRow+num_moves, self.startCol-num_moves))
                        temp_count = 0
                temp_count = (min(7-self.startRow, 7-self.startCol))
                num_moves = 1
                while num_moves <= temp_count >= 0:
                    if board[self.startRow+num_moves][self.startCol+num_moves] == '00':
                        possible_moves.append((self.startRow+num_moves, self.startCol+num_moves))
                        num_moves += 1
                    elif self.same_side(num_moves, num_moves, side, board) is True:
                        temp_count = 0
                    else:
                        possible_moves.append((self.startRow+num_moves, self.startCol+num_moves))
                        temp_count = 0
            if self.pieceMoved == 'wR' or self.pieceMoved == 'bR' or self.pieceMoved == 'wQ' or self.pieceMoved == 'bQ':
                x = self.startCol
                y = self.startRow
                for i in range(1, y+1):          # up
                    if board[self.startRow-i][self.startCol] == '00':
                        possible_moves.append((self.startRow-i, self.startCol))
                    elif self.same_side(-i, 0, side, board) is True:
                        break
                    else:
                        possible_moves.append((self.startRow - i, self.startCol))
                        break
                for i in range(1, 7-(y-1)):     # down
                    if board[self.startRow + i][self.startCol] == '00':
                        possible_moves.append((self.startRow + i, self.startCol))
                    elif self.same_side(i, 0, side, board) is True:
                        print(i)
                        break
                    else:
                        possible_moves.append((self.startRow + i, self.startCol))
                        print(i)
                        break
                for i in range(1, x+1):     # left
                    if board[self.startRow][self.startCol-i] == '00':
                        possible_moves.append((self.startRow, self.startCol-i))
                    elif self.same_side(0, -i, side, board) is True:
                        print(i)
                        break
                    else:
                        possible_moves.append((self.startRow, self.startCol-i))
                        print(i)
                        break
                for i in range(1, 7-(x-1)):     # right
                    if board[self.startRow][self.startCol + i] == '00':
                        possible_moves.append((self.startRow, self.startCol + i))
                    elif self.same_side(0, i, side, board) is True:
                        print(i)
                        break
                    else:
                        possible_moves.append((self.startRow, self.startCol + i))
                        print(i)
                        break                                   # can be simplified, written as one function?

            moves_raw = list(possible_moves)
            for i in range(len(possible_moves)):
                if board[possible_moves[i][0]][possible_moves[i][1]] != '00':
                    possible_captures.append(possible_moves[i])
            if knight_check is True:
                return moves_raw
            return [self.check_for_legality_with_capture_list(moves_raw, self.pieceMoved, possible_captures, start, board, white_to_play), moves_raw]
        return False


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
        self.whiteToPlay = False


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

    def get_notation(self, piece_moved, capture):
        if piece_moved == 'wp' or piece_moved == 'bp':
            if capture is False:
                return self.get_file_rank(self.endRow, self.endCol)
            else:
                return self.files[self.startCol] + 'x' + self.get_file_rank(self.endRow, self.endCol)
        if piece_moved == 'wQ' or piece_moved == 'bQ':
            pass
        return piece_moved + self.get_file_rank(self.startRow, self.startCol) + \
            self.get_file_rank(self.endRow, self.endCol)

    def get_file_rank(self, row, col):
        return self.files[col] + self.ranks[row]

    def check_for_legality(self, legal_moves):
        iterable = 0
        for i in legal_moves:
            legal_moves[iterable] = self.get_file_rank(i[0], i[1])
            iterable += 1
        return legal_moves

    def same_side(self, change_y, change_x, side, board):
        if board[self.startRow + change_y][self.startCol + change_x].startswith(side) is True:
            return True
        return False

    def get_all_possible_moves(self, piece_moved, board):
        possible_moves = []
        if piece_moved == 'wp':
            if board[self.startRow-1][self.startCol] == '00':
                possible_moves.append((self.startRow-1, self.startCol ))
                if self.startRow == 6:
                    possible_moves.append((4, self.startCol))
            if self.startRow != 0:
                if board[self.startRow-1][self.startCol+1] != '00':
                    possible_moves.append((self.startRow-1, self.startCol+1))
            if self.startRow != 7:
                if board[self.startRow-1][self.startCol-1] != '00':
                    possible_moves.append((self.startRow-1, self.startCol-1))
        if piece_moved == 'bp':
            if board[self.startRow+1][self.startCol] == '00':
                possible_moves.append((self.startRow+1, self.startCol ))
                if self.startRow == 1:
                    possible_moves.append((3, self.startCol))
            if self.startRow != 0:
                if board[self.startRow+1][self.startCol+1] != '00':
                    possible_moves.append((self.startRow+1, self.startCol+1))
            if self.startRow != 7:
                if board[self.startRow+1][self.startCol-1] != '00':
                    possible_moves.append((self.startRow+1, self.startCol-1))
        if piece_moved == 'wN' or piece_moved == 'bN':
            if piece_moved == 'wN':
                side = 'w'
            else:
                side = 'b'
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
        return self.check_for_legality(possible_moves)


class Piece:
    def __init__(self, start_square, piece_type, board):
        self.startRow = start_square[0]
        self.startCol = start_square[1]
        self.piece_type = piece_type
        self.board = board




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

    def make_move(self, move):
        self.board[move.startRow][move.startCol] = "00"
        self.board[move.endRow][move.endCol] = move.pieceMoved
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

    def __init__(self, start_square, end_square, board):
        self.startRow = start_square[0]
        self.startCol = start_square[1]
        self.endRow = end_square[0]
        self.endCol = end_square[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

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
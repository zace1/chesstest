
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
import chess


ANALYSIS_TYPES = ['snapshot', 'move', 'game', 'session']


class Metadata:
    def __init__(self):
        self.property_list = []


class MetaBoard(chess.Board):
    def __init__(self, analysis_type, board=None):
        if board:
            self.object_board = board
        else:
            self.object_board = chess.Board.__init__(self)
        assert analysis_type in ANALYSIS_TYPES
        self.analysis_type = analysis_type
        self.metadata = Metadata()

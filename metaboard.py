import chess
import properties


ANALYSIS_TYPES = ['snapshot', 'move', 'game', 'session']
PROPS = properties.__all__


class Metadata:
    def __init__(self):
        self.property_list = []


class MetaBoard(chess.Board):
    def __init__(self, analysis_type, board=None):
        assert analysis_type in ANALYSIS_TYPES

        if board:
            self.object_board = board
        else:
            self.object_board = chess.Board.__init__(self)

        self.analysis_type = analysis_type
        self.metadata = Metadata()
        self.pm = self.object_board.piece_map()
        self.props = {p: None for p in PROPS}

import chess


class MoveAnalysis(object):
    def __init__(self, board: chess.Board, move):
        self.move = move
        self.board = board.push_uci(move)
        """
        if isinstance(move, chess.Move.from_uci()):
            self.piece = board.piece_at(move[0:2])
            self.piece_type = board.piece_type_at(chess.E8, move[0:2])
        if isinstance(move, chess.Move):
            self.piece = move
            """

    @property
    def develops_piece(self, move) -> bool:
        pass

    def pins_piece(self):
        b = self.board
        print(b)
        moves = b.generate_legal_moves()
        attackers_ = chess.Board.attackers(color=WHITE, square=chess.Move.from_uci(self.move).to_square)
        relevant_moves = [x for x in moves if x == chess.Move.from_uci(self.move).to_square]
        return relevant_moves

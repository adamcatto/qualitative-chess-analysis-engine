import chess


def _horizontal_defends(board, defending_square, defended_square) -> bool:
    """
    does piece at `defending_square` defend the `defended_square`?
    """
    assert board.piece_at(defending_square) in [chess.ROOK, chess.QUEEN]
    moves = board.legal_moves
    maybe_defending_moves = [mv for mv in moves if mv.from_square == defending_square]

    def horizontal_move(move: chess.Move) -> bool:
        return chess.square_rank(move.from_square) == chess.square_rank(move.to_square)

    for m in maybe_defending_moves:
        if horizontal_move(m):
            if chess.square_rank(m.to_square) == chess.square_rank(defended_square) and any(
                    chess.square_file(m.to_square) == (chess.square_file(defended_square) - 1),
                    chess.square_file(m.to_square) == (chess.square_file(defended_square) + 1)):
                return True
        else:
            if chess.square_file(m.to_square) == chess.square_file(defended_square) and any(
                    chess.square_rank(m.to_square) == (chess.square_rank(defended_square) - 1),
                    chess.square_rank(m.to_square) == (chess.square_rank(defended_square) + 1)):
                return True

    return False


def back_rank_weakness(board: chess.Board, color: chess.Color) -> bool:
    """
    under threat of a back-rank mate at some point. computed by current state (no rook or queen on back-rank,
    weak squares not defended by player's pieces) and look-ahead in move-tree
    TODO: should there be certain scores for how weak the back rank is? a function of immediacy of threats,
            how many squares are covered, etc.
    """
    pm = board.piece_map()

    if color == chess.BLACK:
        pm = {k: v for k, v in pm.items() if v.symbol() == v.symbol().lower()}
        back_rank = chess.RANK_NAMES[7]
    else:
        pm = {k: v for k, v in pm.items() if v.symbol() == v.symbol().upper()}
        back_rank = chess.RANK_NAMES[0]

    k = [(key, value) for key, value in pm.items() if value.symbol() in ['k', 'K']]
    print(k)
    king_square, king_piece = k[0][0], k[0][1]
    horizontal_positions = {horizontal_square: horizontal for horizontal_square, horizontal in pm.items()
                            if horizontal in [chess.ROOK, chess.QUEEN]}

    back_rank_squares = [chess.square(file, back_rank) for file in chess.FILE_NAMES]

    if king_square not in back_rank_squares:
        return False

    if horizontal_positions:
        for horizontal_square_ in horizontal_positions.keys():
            if chess.square_rank(horizontal_square_) == back_rank \
                    and _horizontal_defends(board, horizontal_square_, king_square):
                return False

    return True

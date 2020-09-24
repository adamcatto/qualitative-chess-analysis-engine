from typing import Union, Set
import collections

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


def absolute_pin(piece, other):
    """
    A pin against the king
    """
    pass


def active(piece) -> bool:
    """
    piece is active if it threatens multiple squares of has a number of squares available for next move
    """
    pass


def advanced_pawn(pawn) -> bool:
    """
    pawn on opponent's side of board
    """
    pass


def advantage(color) -> bool:
    """
    take in factors such as space, time, material, threats
    """
    pass


def alekhine_gun(color) -> bool:
    """
    doubled rooks on file with queen behind them
    procedure:
        if not two rooks and queen on board -> return False
        if not all on same file -> return False
        if not all coordinated -> return False
        if not rook in front of (rook in front of queen) -> return False
        return True
    """
    pass


def arabian_mate() -> bool:
    """
    checkmate when knight and rook trap opponent's king in corner
    """
    pass


def attacking(piece) -> Set:
    """
    Set of squares a piece is attacking
    """
    return collections.Set()


def attacks(piece, other: chess.Square) -> bool:
    """
    if piece attacks a square
    """
    pass


def back_rank_mate() -> bool:
    """
    checkmate from opponent's rook or queen along back rank, where king is unable to move to the second
    rank because all adjacent squares on the second rank are occupied by player's pieces, and there are
    no legal moves to block the rook/queen delivering mate
    """
    pass


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
            if chess.square_rank(horizontal_square_) == back_rank and _horizontal_defends(board, horizontal_square_, king_square):
                return False

        return True


def backward_pawn(pawn) -> bool:
    """
    pawn behind player's other pawn on adjacent file, can't be advanced without support of another pawn
    """
    pass


def bad_bishop(bishop) -> bool:
    """
    bishop behind/defending own pawns
    TODO: should we assign a score to how bad the bishop is? factors include if the pawns have other support,
          how far the bishop can move without x amount of disadvantage, etc.
    """
    pass


def bare_king(color) -> bool:
    """
    only king remains for `color`
    """
    pass


def forced_mate_in_n(board: chess.Board, color_getting_checkmated, num_moves) -> bool:
    """
    for each legal move that `color_getting_checkmated` has, there exists a legal move for the opposing player
    such that after the following move is played, then `forced_mate_in_n(color_getting_checkmated, num_moves - 1)`
    is true.

    that is to say: given alternating color moves at each level in the move tree, every move taken by
    `color_getting_checkmated` has at least one child move (i.e. a move by the opponent) that results in
    `forced_mate_in_n(color_getting_checkmated, num_moves - 1)`, recurse down the tree culminating in a checkmate
    at the end of each path

    TODO: complete this
    """
    if num_moves == 1:
        for mv in board.generate_legal_moves():
            new_board = board.copy()
            new_board.push(mv)
            if new_board.is_checkmate():
                return True
        return False
    else:
        return forced_mate_in_n(board, color_getting_checkmated, num_moves - 1)





def threatening(piece) -> Set:
    """
    set of pieces that `piece` threatens at a given board state
    """
    pass

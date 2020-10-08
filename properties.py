from typing import Union, Set, List, Iterable, Collection
import collections

import chess
import anytree

white_pieces = ['P', 'R', 'N', 'B', 'Q', 'K']
black_pieces = ['p', 'r', 'n', 'b', 'q', 'k']


"""
The goal of this `properties` library is to provide functions which compute information, which is
then to be handed off to functions in the `describe` library. Think of this library as a "backend".

This library mostly computes boolean values, since the `describe` library will mostly communicate 
whether a position or move has a particular feature, such as whether or not there are doubled rooks.
However, sometimes we want to give a more in-depth look at the position; for instance, we may want to 
tell how "open" a position is using a vector of features related to openness of a position. 
"""


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


def absolute_pin(board, piece, other):
    """
    A pin against the king
    """
    pass


def active(board, piece) -> bool:
    """
    piece is active if it threatens multiple squares of has a number of squares available for next move
    """
    pass


def advanced_pawn(board, pawn) -> bool:
    """
    pawn on opponent's side of board
    """
    pass


def advantage(board, color) -> bool:
    """
    take in factors such as space, time, material, threats
    """
    pass


def alekhine_gun(board: chess.Board, color: chess.Color) -> bool:
    """
    doubled rooks on file with queen behind them
    procedure:
        if not two rooks and queen on board -> return False
        if not all on same file -> return False
        if not rook in front of (rook in front of queen) -> return False
        return True
    """
    pm = {k: v.symbol() for k, v in board.piece_map().items()}

    if color == chess.WHITE:
        relevant_pieces = white_pieces
        relevant_case = lambda x: x.upper()
    else:
        relevant_pieces = black_pieces
        relevant_case = lambda x: x.lower()

    piece_count = {piece: 0 for piece, _ in pm.items() for piece in relevant_pieces}

    for square, piece in pm.items():
        if piece in relevant_pieces:
            piece_count[piece] += 1
    if piece_count[relevant_case('r')] < 2 or piece_count[relevant_case('q')] < 1:
        return False

    rook_squares = []
    queen_squares = []

    for key, value in pm.items():
        if value == relevant_case('q'):
            queen_squares.append(key)
        if value == relevant_case('r'):
            rook_squares.append(key)

    if (rook_squares[0] - rook_squares[1]) % 8 != 0:
        return False

    if (((queen_squares[0] - rook_squares[0]) % 8) != 0) or (min(queen_squares[0], min(rook_squares[0], rook_squares[1])) != queen_squares[0]):
        return False

    return True


def arabian_mate(board: chess.Board) -> bool:
    """
    checkmate when knight and rook trap opponent's king in corner
    """
    pass


def attacking(board: chess.Board, piece: chess.Piece) -> Set:
    """
    Set of squares a piece is attacking
    """
    return collections.Set()


def attacks(board, piece, other: chess.Square) -> bool:
    """
    if piece attacks a square
    """
    pass


def back_rank_mate(board) -> bool:
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


def backward_pawn(board, pawn) -> bool:
    """
    pawn behind player's other pawn on adjacent file, can't be advanced without support of another pawn
    """
    pass


def bad_bishop(board, bishop) -> bool:
    """
    bishop behind/defending own pawns
    TODO: should we assign a score to how bad the bishop is? factors include if the pawns have other support,
          how far the bishop can move without x amount of disadvantage, etc.
    """
    pass


def bare_king(board, color) -> bool:
    """
    only king remains for `color`
    """
    pass


def battery(board, color) -> bool:
    """
    any(double rooks on (file v rank), double rook and queen on (file v rank), place bishop and queen on diagonal)

    at least two continuously-moving pieces attacking/x-raying same square
    """
    pass


def battery_king(board, color) -> bool:
    """
    battery AND lined up with king
    """
    pass


def bind(board, color) -> bool:
    """
    tension, player doesn't have many moves to make, tough to break out. situations:

    * advanced pawns

    TODO: enumerate situations / situation-combos, figure out how to represent them
    """
    pass


def bishop_pair(board, color) -> bool:
    """
    player has two bishops, opponent does not
    """
    pass


def blockade(board, color) -> bool:
    """
    piece in front of enemy pawn, stopping its advancement

    TODO: should we have another function for generating blockade feature vector, like with `open_position`?
    TODO: should there be "verbose mode" for applying feature vector functions?
    """
    pass


def break_move(board, move) -> bool:
    """
    a break – typically a pawn move that gains space
    """
    pass


def breakthrough(board, move) -> bool:
    """
    destroy defensive structure
    """
    pass


def bridge(board, color) -> bool:
    """
    path for king in endgame by providing cover against checks from line pieces
    """
    pass


def can_opener(board, move) -> bool:
    """
    attacking kingside by advancing the h-pawn (to open file near defender's king)

    TODO: should we make something similar for queenside + a-pawn?
    TODO: can-opener refutation? e.g. previous move was can-opener, current move blockades the can-opener pawn?
    """
    pass


def centralization(board, move_sequence: Union[chess.Move, Iterable[chess.Move]]) -> bool:
    """
    moving piece(s) to center of board
    """
    if isinstance(move_sequence, chess.Move):
        move_sequence = [move_sequence]
    # temporary return; TODO: actually implement
    return False


def centralization_feature_vector(board, move_sequence: Union[chess.Move, Iterable[chess.Move]]) -> List:
    """
    returns vector of features describing along what dimensions a move sequence is centralizing
    """
    if isinstance(move_sequence, chess.Move):
        move_sequence = [move_sequence]
    # temporary return; TODO: actually implement
    return []


def cheapo(board, move) -> bool:
    """
    determines whether a move is a cheapo – hoping that an opponent will be too weak to see that the move
    is actually a bad move, a "primitive trap"

    TODO: should this be hand-crafted (e.g. using move tree + evaluation), searched in database of openings, combo, or more?
    """
    pass


def closed(board) -> bool:
    """
    determines whether or not a position is closed. similar to open.
    """
    pass


def closed_feature_vector(board) -> List:
    """
    similar to open feature vector. properties:

    * interlocking pawn chains
    * few exchange opportunities
    * extensive maneurvering behind lines
    """


def combination(board, move_sequence) -> bool:
    """
    characterized by a constrained space of move-sequences (paths on the move tree) yielding an advantage
    """
    pass


def connected_pawns(board, color, pawns: Collection) -> bool:
    """
    two or more pawns of same color on adjacent files
    """
    pass


def connected_passed_pawns(board, color, pawns: Collection) -> bool:
    """
    pawns are both passed pawns and connected.

    procedure:
        pawn_1 is passed_pawn
        pawn_2 is passed_pawn
        pawns are connected
    """
    pass


def connected_rook(board, color, rooks: Collection) -> bool:
    """
    rooks on same rank or file without pieces in between them
    """
    pass


def consolidation(board, move_sequence) -> bool:
    """
    improving position by repositioning piece(s) to better square(s), e.g.

    * connecting/coordinating pieces
    * improving king safety
    * activating pieces
    * moving heavy pieces to more secure squares
    """
    pass


def control_of_center(board, color) -> bool:
    """
    does player control center?
    """
    pass


def control_of_center_feature_vector(board, color) -> List:
    """
    to what extent and in what ways does player control center?
    """
    pass


def control_pawn(board, color, pawn, square=None, file=None, rank=None) -> bool:
    """
    does a pawn control a square
    """
    assert not all(square=None, file=None, rank=None)
    # temporary; TODO: actually implement
    return False


def corresponding_squares(board, squares: Collection) -> bool:
    """
    squares such that when king moves to one square, opponent's king must go to other (corresponding) square to hold position
    """
    pass


def counterplay(board, move) -> bool:
    """
    when opponent has made aggressive moves recently, player responds by making similarly aggressive moves
    """
    pass


def cover(board, move) -> bool:
    """
    move that protects a piece or controls a square
    """
    pass


def cramped(board) -> bool:
    """
    position in which pieces have very few squares to go to on average
    """
    pass


def cramped_feature_vector(board) -> List:
    """
    feature vector describing in what ways the position is cramped. e.g.:

    * one side's average number of legal moves (outside of a check position) per piece is small
    * distribution of legal moves per piece fits certain criteria
    * large number of blockades / locked pawns
    """
    pass


def critical_square(board, square) -> bool:
    """
    an important square in a position
    TODO: how to implement this
    """
    pass


def critical_position(board) -> bool:
    """
    position in which evaluation shows that advantage structure is about to change

    may be done with combo of eval engine and mining move tree to determine if space of moves keeping
    advantage structure the same is small
    """
    pass


def cross_check(board, move) -> bool:
    """
    respond to check with a check.
    previous move was a check, current move gets out of check with move that also puts opponent in check
    """
    pass


def decoy(board, move) -> bool:
    """
    tactic used to lure a piece to particular squaree.

    can be characterized by short-sighted gain, e.g. check or winning material, but looking far enough ahead
    shows that this is a mistake
    """
    pass


def defensive_move(board, move) -> bool:
    """
    response to an attack that defends piece
    """
    pass


def deflect(board, move) -> bool:
    """
    luring a piece away from a good square. cf. oveerloading
    """
    pass


def desperado(board, piece, move_sequence=None) -> bool:
    """
    * threatened piece sacrificing itself for maximum compensation
    * ––

    TODO: should this be looked for only when move sequence is available? in model-based sequence case, not static case
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
    root = anytree.AnyNode(id='root')
    if num_moves == 1:
        for mv in board.generate_legal_moves():
            new_board = board.copy()
            new_board.push(mv)
            if new_board.is_checkmate():
                return True
        return False
    else:

        for mv in board.generate_legal_moves():
            new_board = board.copy()
            new_board.push(mv)

        return forced_mate_in_n(board, color_getting_checkmated, num_moves - 1)


def open_position(board) -> bool:
    """
    features:

    * lack of central pawns
    * degree of support amongst central pawns

    ========

    maybe something like relu where hitting a threshold of features returns True, else False
    """
    pass


def open_position_feature_vector(board) -> List:
    """
    returns a feature vector numerically describing the dimensions along which a position is open.

    ideas:

    * number of central pawns
    * degree of support amongst central pawns
    """
    return []


def threatening(piece) -> Set:
    """
    set of pieces that `piece` threatens at a given board state
    """
    pass

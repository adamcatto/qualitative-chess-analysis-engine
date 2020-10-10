from typing import Union, Set, List, Iterable, Collection, Tuple, Callable, Dict
import collections

import chess
import anytree


__all__ = ['absolute_pin', 'active', 'advanced_pawn', 'advantage', 'alekhine_gun', 'arabian_mate', 'attacking',
           'attacks', 'back_rank_mate', 'back_rank_weakness', 'backward_pawns', 'bad_bishop', 'bare_king', 'battery',
           'battery_king', 'bind', 'bishop_pair', 'blockade', 'break_move', 'breakthrough', 'bridge', 'can_opener',
           'centralization', 'centralization_feature_vector', 'cheapo', 'closed', 'closed_feature_vector', 'combination',
           'connected_pawns', 'connected_passed_pawns', 'connected_rook', 'consolidation', 'control_of_center',
           'control_of_center_feature_vector', 'control_pawn', 'corresponding_squares', 'counterplay', 'cover',
           'cramped', 'cramped_feature_vector', 'critical_square', 'critical_position', 'cross_check', 'decoy',
           'defensive_move', 'deflect', 'desperado', 'discovered_attack', 'discovered_check', 'double_attack',
           'double_check',
           'doubled_pawns', 'edge', 'en_prise', 'en_passant', 'escape_square', 'exposed_king', 'family_fork',
           'fianchetto', 'fianchetto_squares', 'forced_mate_in_n', 'forced_move', 'fork', 'fortress', 'gambit_move',
           'good_bishop', 'greek_gift_sacrifice', 'half_open_file', 'hanging_pawns', 'hole', 'horwitz_bishops',
           'hypermodern_position', 'imbalance_feature_vector', 'inactive', 'initiative', 'interference', 'intermezzo',
           'isolani', 'isolated_pawn', 'italian_bishop', 'kick', 'king_hunt', 'king_walk', 'liquidation', 'loose_piece',
           'lucena_position', 'luft', 'majority', 'maroczy_bind', 'material_style', 'material_style_feature_vector',
           'open_position', 'open_position_feature_vector', 'pin', 'poisoned_pawn', 'positional_sacrifice', 'promotion',
           'promoted_to', 'pseudo_sacrifice', 'quiet_move', 'romantic_style', 'rook_lift', 'sacrifice', 'sham_sacrifice',
           'skewer', 'smothered_mate', 'spanish_bishop', 'squeeze', 'support_point', 'tension', 'threatening',
           'triangulation', 'tripled_pawns', 'undermining', 'unpinning', 'vacating_sacrifice', 'valve',
           'vanished_center', 'waiting_move', 'weak_square', 'windmill', 'wrong_rook_pawn', 'x_ray', 'zugzwang']


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


def _relevant_pieces_cases(color) -> Tuple[List, Callable]:
    if color == chess.WHITE:
        relevant_pieces = white_pieces
        relevant_case = lambda x: x.upper()
    else:
        relevant_pieces = black_pieces
        relevant_case = lambda x: x.lower()
    return relevant_pieces, relevant_case


def _filter_piece_map_by_color(pm, color) -> Dict[chess.Square, chess.Piece]:
    if color == chess.BLACK:
        pm = {k: v for k, v in pm.items() if v.symbol() == v.symbol().lower()}
    else:
        pm = {k: v for k, v in pm.items() if v.symbol() == v.symbol().upper()}
    return pm


def _infer_color_from_piece(board, piece: chess.Piece) -> chess.Color:
    pass


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

    relevant_pieces, relevant_case = _relevant_pieces_cases(color)
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


def backward_pawns(board: chess.Board, piece_map: Dict[chess.Square, chess.Piece],
                   color: chess.Color) -> List[Tuple[chess.FILE_NAMES, chess.Square]]:
    """
    pawn behind player's other pawns on adjacent file, can't be advanced without support of another pawn
    """
    backward_pawn_list = []
    relevant_pieces, relevant_case = _relevant_pieces_cases(color)
    pm = _filter_piece_map_by_color(piece_map, color)
    pawn_map: Dict[chess.Square, chess.Piece] = {k: v for k, v in pm.items() if v.symbol() == relevant_case('p')}

    for square, pawn in pawn_map:
        left_right = (False, False)
        square_file, square_rank = chess.square_file(square), chess.square_rank(square)
        left_file, right_file = square_file - 1, square_file + 1

        for square_, pawn_ in pawn_map:
            if chess.square_file(square_) == left_file:
                if chess.square_rank(square_) > square_rank:
                    left_right[0] = True
                else:
                    break
            elif chess.square_file(square_) == right_file:
                if chess.square_rank(square_) > square_rank:
                    left_right[1] = True
                else:
                    break

        if left_right == (True, True):
            backward_pawn_list.append((square, pawn))

    return backward_pawn_list


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


def discovered_attack(board, move) -> bool:
    """
    moving piece such that other piece it was blocking attacks a piece
    """
    pass


def discovered_check(board, move) -> bool:
    """
    discovered attack on king
    """
    pass


def double_attack(board, move) -> bool:
    """
    one move creates two new attacks.

    idea: difference between attacking set before `move` and attacking set after `move`
    """
    pass


def double_check(board, move) -> bool:
    """
    double attack such that both new attacks are on king
    """
    pass


def doubled_pawns(board, color) -> bool:
    """
    two pawns of same color on same file
    """
    pass


# TODO: dynamic play?


def edge(board) -> chess.Color:
    """
    small advantage, returns chess.Color representing player who has edge
    """
    pass


def en_prise(board) -> chess.Square:
    """
    hanging piece
    """
    pass


def en_passant(board, move) -> bool:
    """
    en passant capture
    """
    pass


def escape_square(board, square: chess.Square) -> bool:
    """
    square on second rank for king to run to in case of back-rank check
    """
    pass


EXPANDED_CENTER = (file + rank for file in ['c', 'd', 'e', 'f'] for rank in ['3', '4', '5', '6'])


def exposed_king(board, color) -> bool:
    """
    king lacks adjacent pawns to shield it from attack
    """
    pass


def family_fork(board) -> bool:
    """
    knight fork simultaneously checking and attacking queen
    """
    pass


def fianchetto(board, bishop) -> bool:
    """
    bishop on long diagonal (b2/g2 – white; b7/g7 – black)

    idea: nope until you see B{b2,g2,b7,g7} in move sequence, then update board metadata (MetaBoard class);
    update MetaBoard upon seeing bishop moving away from that square
    """
    pass


def fianchetto_squares(board) -> Collection:
    """
    return squares on which bishops are fianchettoed
    """
    return collections.Set()


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


def forced_move(board, move) -> bool:
    pass


def fork(board, move) -> bool:
    pass


def fortress(board) -> bool:
    pass


def gambit_move(board, move) -> bool:
    pass


def good_bishop(board, bishop) -> bool:
    pass


def greek_gift_sacrifice(board) -> bool:
    """
    Bxh7+, Bxh2+ (white – similar for black) against castled king
    """
    pass


def half_open_file(board, color, file) -> bool:
    """
    file on which only one player has no pawns
    """
    pass


def hanging_pawns(board, pawns) -> bool:
    """
    same color pawns on adjacent files, without pawns of same color on files to their sides
    """
    pass


def hole(board, square) -> bool:
    """
    square inside player's side of the board that cannot be controlled by pawn (pawns passed
    on both adjacent files)
    """
    pass


def horwitz_bishops(board, bishops) -> bool:
    """
    player's bishops controlling adjacent diagonals
    """
    pass


def hypermodern_position(board) -> bool:
    """
    controlling center with pieces from flanks, rather than occupying center with pawns
    """
    pass


def imbalance_feature_vector(board) -> List:
    """
    feature vector consisting of ways in which there exists an imbalance, e.g.
    central pawns, bishop pair, strong/weak bishop, connected rooks, space, etc.
    """
    pass


def inactive(board, piece) -> bool:
    return not active(board, piece)


def initiative(board, color) -> bool:
    pass


def interference(board, move) -> bool:
    """
    interruption of line or diagonal betweeen attacked piecee and its defender using an interposing piece
    """
    pass


def intermezzo(board, move) -> bool:
    """
    cf. intermediate move, zwischenzug
    """
    pass


def isolani(board, pawn) -> bool:
    """
    isolated d-pawn
    """
    pass


def isolated_pawn(board, pawn) -> bool:
    """
    pawn without same color pawns on adjacent files
    """
    pass


def italian_bishop(board, bishop) -> bool:
    """
    white/black bishop developed to c4/c5
    """
    pass


def kick(board, move, square) -> bool:
    """
    attacking piece on square with `move` such that the piece has to move
    """
    pass


def king_hunt(board, move_sequence) -> bool:
    """
    sequence of attacks on king such that it has to move far from original position
    """
    pass


def king_walk(board, move_sequence) -> bool:
    """
    sequence of king moves such that king gets to safer square

    TODO: do we really need board parameter? doesn't seem like it fits...
    """
    pass


def liquidation(board, move_sequence) -> bool:
    """
    simplification
    """
    pass


def loose_piece(board, piece) -> bool:
    """
    piece vulnerable to opponent attacks b/c it is undefended and cannot easily be withdrawn or supported
    """
    pass


def lucena_position(board) -> bool:
    """
    look it up
    """
    pass


def luft(board, move) -> bool:
    """
    is move a luft?
    """
    pass


def majority(board, color) -> bool:
    """
    player has larger number of pawns on one flank than opponent does
    """
    pass


def maroczy_bind(board) -> bool:
    """
    bind on light squares in center – typically d5, by placing pawns on c4 and e4
    """
    pass


def material_style(board, move_sequence) -> bool:
    pass


def material_style_feature_vector(board, move_sequence) -> List:
    pass


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


def pin(board, piece, other_piece) -> bool:
    pass


def poisoned_pawn(board, pawn) -> bool:
    pass


def positional_sacrifice(board, move) -> bool:
    pass


def promotion(board, move) -> bool:
    pass


def promoted_to(board, move) -> chess.Piece:
    pass


def pseudo_sacrifice(board, move) -> bool:
    pass


def quiet_move(board, move) -> bool:
    pass


def romantic_style(board, move_sequence) -> bool:
    pass


def rook_lift(board, move) -> bool:
    pass


def sacrifice(board, move) -> bool:
    pass


def sham_sacrifice(board, move) -> bool:
    pass


def skewer(board, move) -> bool:
    pass


def smothered_mate(board, move) -> bool:
    pass


def spanish_bishop(board, bishop) -> bool:
    """
    white bishop on b5
    """
    pass


def squeeze(board, pawn_move) -> bool:
    pass


def support_point(board, square) -> bool:
    """
    square that cannot be attacked by a pawn
    """
    pass


def tension(board) -> List:
    """
    A position in which there are one or more exchanges possible. Represented as

    * how many possible exchanges there are
    * what the exchange combos are
    * what squares are involveed
    """
    pass


# TODO: implement `thematic` move?


def threatening(piece) -> Set:
    """
    set of pieces that `piece` threatens at a given board state
    """
    pass


def triangulation(board, move_sequence) -> bool:
    """
    A technique used in king and pawn endgames (less commonly seen with other pieces) to lose a tempo and gain the opposition
    """
    pass


def tripled_pawns(board) -> bool:
    pass


def undermining(board, move) -> bool:
    pass


def unpinning(board, move) -> bool:
    pass


def vacating_sacrifice(board, move) -> bool:
    pass


def valve(board, move) -> bool:
    pass


def vanished_center(board) -> bool:
    pass


def waiting_move(board, move) -> bool:
    pass


def weak_square(board, square, color) -> bool:
    pass


def windmill(board, move_sequence) -> bool:
    pass


def wrong_rook_pawn(board, pawn) -> bool:
    pass


def x_ray(board, attacking_piece, attacked_piece) -> bool:
    pass


def zugzwang(board, color) -> bool:
    pass

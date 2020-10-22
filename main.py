import chess
import chess.pgn
from io import StringIO

from properties import alekhine_gun, forced_mate_in_n


board_ = chess.Board()
board_.push_san('e4')
board_.push_san('Nc6')

print(board_)
#print(back_rank_weakness(board_, chess.WHITE))
pm = board_.piece_map()
pm = {k: v.symbol() for k, v in pm.items()}

print(alekhine_gun(board_, chess.WHITE))
board1 = chess.Board()
board1.set_board_fen('4r1k1/2rq1npp/2p1p3/3p4/pP1P4/P1R1PPP1/2R2KBP/2Q5')
print('\n\n')
print(board1)
print(alekhine_gun(board1, chess.WHITE))
#print(forced_mate_in_n(board1, chess.BLACK, 5))

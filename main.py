import chess
from move_analysis.moves import MoveAnalysis
from properties import back_rank_weakness


board_ = chess.Board()
board_.push_san('e4')
board_.push_san('d5')

print(board_)
print(back_rank_weakness(board_, chess.WHITE))
pm = board_.piece_map()
pm = {k: v.symbol() for k, v in pm.items()}
print(pm)

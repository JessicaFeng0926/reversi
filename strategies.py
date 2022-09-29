import random
from typing import List, Tuple

from board import Board
from cell import Cell

def get_corner_best_move(board: Board) -> Cell:
    '''优先选择抢角，没有角就选得分最高的'''
    valid_moves: List[Tuple[Cell,int]] = board.get_valid_moves()
    random.shuffle(valid_moves)

    # 抢角
    for cell, _ in valid_moves:
        if board.is_on_corner(cell):
            return cell
    
    # 抢不到角，抢最高分
    best_move: Tuple[Cell,int] = max(valid_moves,key=lambda m:m[1])
    return best_move[0]

def get_random_move(board: Board) -> Cell:
    '''随便下'''
    valid_moves: List[Tuple[Cell,int]] = board.get_valid_moves()
    return random.choice(valid_moves)[0]


def get_worst_move(board: Board) -> Cell:
    '''选择最差的格子下棋'''
    valid_moves: List[Tuple[Cell,int]] = board.get_valid_moves()
    random.shuffle(valid_moves)
    
    # 先尽量选非角落并且分数最低的
    worst_score: int = 64
    worst_cell: Cell = None
    for cell,score in valid_moves:
        # 如果这个格子是角落里的，那就先越过去
        if board.is_on_corner(cell):
            continue
        if score < worst_score:
            worst_score = score
            worst_cell = cell
    
    if worst_cell:
        return worst_cell
    # 如果可以走的格子只有角落里的,那就选一个角落里分数最低的返回
    worst_move =  min(valid_moves,key=lambda m:m[1])
    return worst_move[0]

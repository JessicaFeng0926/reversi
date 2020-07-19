#from __future__ import annotations
from enum import Enum
import settings

class Piece(Enum):
    '''棋子类'''
    # 黑子
    B = 'B'
    # 白子
    W = 'W'
    # 空
    E = 'E'

    @property
    def opposite(self) -> 'Piece':
        '''翻转棋子'''
        if self == Piece.B:
            return Piece.W
        elif self == Piece.W:
            return Piece.B
        else:
            return Piece.E




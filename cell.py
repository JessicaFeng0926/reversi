import pygame

from piece import Piece
import settings

class Cell:
    '''棋盘上的一个格子'''
    def __init__(self, x: int, y: int, size: int) -> None:
        '''用左上角横坐标、纵坐标和边长初始化一个空格子'''
        self._rect = pygame.Rect(x,y,size,size)
        self._piece = Piece.E

    def get_rect(self) -> pygame.Rect:
        '''获取这个格子的矩形'''
        return self._rect

    def set_piece(self, piece: Piece) -> None:
        '''更新这个格子里的棋子'''
        self._piece = piece
        
    
    def draw_piece(self, surface: pygame.Surface) -> None:
        '''把棋子画在这个格子里'''
        piece = self._piece
        # 棋子颜色
        color = settings.BLACK if piece == Piece.B else settings.WHITE
        # 格子的矩形
        rect = self._rect
        # 圆心
        center = (int(rect.centerx), int(rect.centery))
        # 在这个格子里绘制一个棋子
        pygame.draw.circle(surface,color,center,settings.PIECE_RADIUS,0)

    def get_piece(self) -> Piece:
        '''获取这个格子里的棋子'''
        return self._piece

    
from typing import List, Tuple

import pygame

from cell import Cell
from piece import Piece
import settings

class Board:
    '''棋盘类'''
    def __init__(self) -> None:
        self._container: List[List[Cell]]= []
        for row in range(8):
            row_of_board = []
            for col in range(8):
                row_of_board.append(
                    Cell(settings.LEFT_OF_BOARD + col*settings.CELL_SIZE,
                         settings.TOP_OF_BOARD + row*settings.CELL_SIZE,
                         settings.CELL_SIZE)
                    )
            self._container.append(row_of_board)
        # 默认黑棋先走
        self._turn = Piece.B
        # 中间的四个格子先摆上棋子
        self._container[3][3].set_piece(Piece.B)
        self._container[4][4].set_piece(Piece.B)
        self._container[3][4].set_piece(Piece.W)
        self._container[4][3].set_piece(Piece.W)
    
    @property
    def turn(self) -> Piece:
        '''获取当前掌握出牌权的棋子'''
        return self._turn
    
    def change_turn(self) -> None:
        '''交出出牌权'''
        self._turn = self._turn.opposite

    def draw_board(self, surface) -> None:
        '''把棋盘绘制到屏幕上'''
        # 先绘制绿色背景
        pygame.draw.rect(surface, settings.GREEN, (settings.LEFT_OF_BOARD,settings.TOP_OF_BOARD,settings.BOARD_SIZE,settings.BOARD_SIZE))

        # 再绘制每个黑色边框的透明小格子,以及格子里的棋子(如果有的话)
        for row_of_board in self._container:
            for cell in row_of_board:
                pygame.draw.rect(surface, settings.BLACK, cell.get_rect(), 1)
                piece = cell.get_piece()
                if piece != Piece.E:
                    cell.draw_piece(surface)
    
    def is_on_board(self, x: float, y: float) -> bool:
        '''判断鼠标点击的点是否在棋盘上'''
        return x >= settings.LEFT_OF_BOARD and x < settings.LEFT_OF_BOARD + settings.BOARD_SIZE \
            and y >= settings.TOP_OF_BOARD and y < settings.TOP_OF_BOARD + settings.BOARD_SIZE
    
    def is_valid_row_col(self, row: int, col: int) -> bool:
        '''判断给定的行和列是否是有效的'''
        return row >= 0 and row < 8 and col >= 0 and col < 8
    
    def is_on_corner(self,cell: Cell) -> bool:
        '''判断给定的格子是否在角落'''
        rect = cell.get_rect()
        col = (rect.x - settings.LEFT_OF_BOARD)//settings.CELL_SIZE
        row = (rect.y - settings.TOP_OF_BOARD)//settings.CELL_SIZE
        return (row == 0 or row == 7) and (col == 0 or col == 7)
    
    def is_full(self) -> bool:
        '''判断棋盘是否已经满了'''
        for row_of_board in self._container:
            for cell in row_of_board:
                if cell.get_piece() == Piece.E:
                    return False
        return True

    def get_cell_by_coordinates(self, x: float, y: float) -> Cell:
        '''根据鼠标的坐标返回鼠标点击的格子'''
        for row_of_board in self._container:
            for cell in row_of_board:
                rect = cell.get_rect()
                if  x >= rect.left and x < rect.right and y >= rect.top and y < rect.bottom:
                    return cell
        
    
    def get_cells_to_flip(self, cell: Cell) -> List[Cell]:
        '''判断在当前的格子下棋能翻转哪些格子的棋子'''
        # 如果当前格子已经有棋子了，不合法，不会翻转任何棋子
        if cell.get_piece() != Piece.E:
            return []
        
        # 下面这个列表存放将要被翻转的棋子
        cells_to_flip: List[Cell]= []
        
        # 获取这个格子的矩形
        rect = cell.get_rect()
        # 获取这个格子在棋盘里的列和行
        col_start = (rect.x - settings.LEFT_OF_BOARD)//settings.CELL_SIZE
        row_start = (rect.y - settings.TOP_OF_BOARD)//settings.CELL_SIZE
        
        # 对手的棋子
        op_piece = self._turn.opposite

        # 上，下，左，右，左上，左下，右上，右下八个方向
        # 只要挨着的还是对手的棋子，就一直沿着这个方向走
        for row_step, col_step in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,-1),(-1,1),(1,1)]:
            row = row_start +  row_step
            col = col_start + col_step
            while self.is_valid_row_col(row, col) and self._container[row][col].get_piece() == op_piece:
                row += row_step
                col += col_step
            # 如果结束之后依然是有效的行列，并且这个格子是自己的棋子
            # 就要反着走，把一路上的要翻转的棋子都添加到列表里
            if self.is_valid_row_col(row,col) and self._container[row][col].get_piece() == self._turn:
                row -= row_step
                col -= col_step
                while not (row == row_start and col == col_start):
                    cells_to_flip.append(self._container[row][col])
                    row -= row_step
                    col -= col_step
        # 返回要翻转的棋子，也可能一个棋子也没有
        return cells_to_flip

    def make_move_by_coordinates(self,x,y) -> None:
        '''根据坐标下棋,这是给玩家用的'''
        if self.is_on_board(x,y):
            cell = self.get_cell_by_coordinates(x,y)
            cells_to_flip = self.get_cells_to_flip(cell)
            if cells_to_flip:
                cell.set_piece(self._turn)
                for c in cells_to_flip:
                    c.set_piece(self._turn)
                # 把出牌权交给对方
                self._turn = self._turn.opposite
        

    def make_move_by_cell(self,cell: Cell) -> None:
        '''根据选好的格子下棋，这是给电脑用的'''
        # 一定要先获取要翻转的棋，然后再往各个格子里放棋子
        # 否则就无法获取要翻转的棋了
        cells_to_flip = self.get_cells_to_flip(cell)
        for c in cells_to_flip:
            c.set_piece(self._turn)
        cell.set_piece(self._turn)
        # 把出牌权交给对方
        self._turn = self._turn.opposite
    
    def get_valid_moves(self) -> List[Tuple[Cell,int]]:
        '''获取当前状态下，所有能够下棋的格子，以及在这个格子上能翻转多少个棋子'''
        valid_moves: List[Tuple[Cell,int]] = []
        for row_of_board in self._container:
            for cell in row_of_board:
                cells_to_flip = self.get_cells_to_flip(cell)
                if cells_to_flip:
                    valid_moves.append((cell,len(cells_to_flip)))
        return valid_moves

    def show_hints(self, font: pygame.font.Font, surface: pygame.Surface) -> None:
        '''给用户展示提示'''
        valid_moves = self.get_valid_moves()
        for cell, num in valid_moves:
            text = font.render(str(num),True,settings.BLACK)
            text_rect = text.get_rect()
            cell_rect = cell.get_rect()
            text_rect.centerx = cell_rect.centerx
            text_rect.centery = cell_rect.centery
            surface.blit(text,text_rect)
    
    def get_score(self) -> Tuple[int,int]:
        '''返回玩家和电脑的分数'''
        player_score = 0
        computer_score = 0
        for row_of_board in self._container:
            for cell in row_of_board:
                if cell.get_piece() == Piece.B:
                    player_score += 1
                elif cell.get_piece() == Piece.W:
                    computer_score += 1
        return player_score, computer_score







        
    
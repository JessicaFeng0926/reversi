import sys, os
from typing import Tuple

import pygame
import pygame.locals as pl

from board import Board
from piece import Piece
import settings
from strategies import get_corner_best_move,get_random_move,get_worst_move

# 初始化pygame
pygame.init()
main_clock = pygame.time.Clock() 

# 设置窗口
window_surface = pygame.display.set_mode((settings.WINDOW_WIDTH,settings.WINDOW_HEIGHT))
pygame.display.set_caption('翻转棋')

# 设置大小两种字体
small_font = pygame.font.SysFont(None,32)
big_font = pygame.font.SysFont(None,64)

# 加载音乐文件
MEDIA_PATH = os.path.join(settings.BASE_DIR,'media')
pygame.mixer.music.load(os.path.join(MEDIA_PATH,'planB.mp3'))
win_sound = pygame.mixer.Sound(os.path.join(MEDIA_PATH,'win.wav'))
tie_sound = pygame.mixer.Sound(os.path.join(MEDIA_PATH,'tie.wav'))
lose_sound = pygame.mixer.Sound(os.path.join(MEDIA_PATH,'gameover.wav'))




def play_game() -> Tuple[int, int]:
    '''这是一局游戏，会返回最终的比分'''
    # 创建棋盘
    board = Board()

    # 下面的布尔值表示音乐和提示的开启或关闭，默认开启
    play_music = True
    show_hints = True

    # 播放音乐
    pygame.mixer.music.play(-1,0.0)
    
    while True:
        # 棋盘满了，结束游戏
        if board.is_full():
            if play_music:
                pygame.mixer.music.stop()
            return board.get_score()
        
        # 这里主要检查的是玩家是否有棋课下
        if not board.get_valid_moves():
            board.change_turn()
            if not board.get_valid_moves():
                if play_music:
                    pygame.mixer.music.stop()
                return board.get_score()

        for event in pygame.event.get():
            if event.type == pl.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pl.KEYUP:
                if event.key == pl.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pl.K_h:
                    # 开关提示功能
                    show_hints = not show_hints
                if event.key == pl.K_m:
                    if play_music:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1,0.0)
                    play_music = not play_music

            if event.type == pl.MOUSEBUTTONDOWN:
                if board.turn == Piece.B:
                    #if board.get_valid_moves():
                    x,y = event.pos[0],event.pos[1]
                    board.make_move_by_coordinates(x,y)
                    # 玩家没有棋可以下了，就把出牌权交给电脑
                    #else:
                        #board.change_turn()
                        #if not board.get_valid_moves():
                            #playing = False
        
        
        
        
        # 如果轮到电脑出牌，就自动出
        # 电脑没有棋可以下了，就把出牌权交给玩家
        if board.turn == Piece.W:
            if board.get_valid_moves():
                cell = get_worst_move(board)
                board.make_move_by_cell(cell)
            else:
                board.change_turn()
                if not board.get_valid_moves():
                    if play_music:
                        pygame.mixer.music.stop()
                    return board.get_score()
                    
        
        # 清屏，重新绘制棋盘
        window_surface.fill(settings.WHITE)
        board.draw_board(window_surface)
        # 如果提示功能开启了，并且现在轮到玩家的黑子下棋，就显示提示
        if show_hints and board.turn == Piece.B:
            board.show_hints(small_font,window_surface)
        # 刷新屏幕
        pygame.display.update()
        main_clock.tick(settings.FPS)


def show_results(player_score,computer_score) -> None:
    '''根据最终比分在屏幕上显示文字'''
    if player_score > computer_score:
        word = 'You Win'
        bg_color = settings.GREEN
        win_sound.play()
    elif player_score < computer_score:
        word = 'You Lose'
        bg_color = settings.RED
        lose_sound.play()
    else:
        word = 'Tie'
        bg_color = settings.BLUE
        tie_sound.play()
    window_surface.fill(settings.WHITE)
    # 显示结论
    text = big_font.render(word,True,settings.BLACK,bg_color)
    text_rect = text.get_rect()
    text_rect.centerx = window_surface.get_rect().centerx
    text_rect.centery = window_surface.get_rect().centery-50
    window_surface.blit(text,text_rect)
    # 显示比分
    score = small_font.render(f'{player_score} VS {computer_score}',True,settings.BLACK)
    score_rect = score.get_rect()
    score_rect.centerx = window_surface.get_rect().centerx
    score_rect.centery = window_surface.get_rect().centery + 50
    window_surface.blit(score,score_rect)
    pygame.display.update()

def play_again() -> bool:
    '''玩家决定是否再玩一盘'''
    while True:
        for event in pygame.event.get():
            if event.type == pl.QUIT:
                return False
            if event.type == pl.KEYUP:
                if event.key == pl.K_ESCAPE:
                    return False
                else:
                    return True

if __name__ == '__main__':
    while True:
        # 玩一盘，获取最终的得分
        player_score, computer_score = play_game()
        # 根据最终得分显示胜利或者失败的结果
        show_results(player_score,computer_score)
        # 等待用户选择再来一盘或者退出游戏
        if not play_again():
            pygame.quit()
            sys.exit()


        

        
        
    






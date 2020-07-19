import sys, os
from typing import Tuple, Callable

import pygame
import pygame.locals as pl


from board import Board
from piece import Piece
import settings
from strategies import get_corner_best_move,get_random_move,get_worst_move

 
def terminate() -> None:
    '''关闭游戏'''
    pygame.quit()
    sys.exit()

def write_text(font: pygame.font.Font, 
               text: str, 
               color: Tuple[int,int,int],
               centerx: int, 
               centery: int,
               surface: pygame.Surface,
               bg_color = None) -> None:
    ''''写文字'''
    text_obj = font.render(text,True,color,bg_color)
    text_rect = text_obj.get_rect()
    text_rect.centerx = centerx
    text_rect.centery = centery
    surface.blit(text_obj,text_rect)

def welcome() -> Tuple[pygame.Rect,pygame.Rect,pygame.Rect]:
    '''开始界面，有选择难度的按钮'''
    window_surface.fill(settings.WHITE)
    write_text(big_font,
              'Reversi',
              settings.BLACK,
              window_rect.centerx,
              window_rect.centery-100,
              window_surface)
    write_text(small_font,
               'Please choose a difficult level',
               settings.BLACK,
               window_rect.centerx,
               window_rect.centery-20,
               window_surface)
    easy_rect = pygame.Rect(100,300,300,70)
    medium_rect = pygame.Rect(100,380,300,70)
    hard_rect= pygame.Rect(100,460,300,70)
    pygame.draw.rect(window_surface,settings.GREEN,easy_rect,0)
    pygame.draw.rect(window_surface,settings.GREEN,medium_rect,0)
    pygame.draw.rect(window_surface,settings.GREEN,hard_rect,0)
    write_text(small_font,
               'Easy',
               settings.BLACK,
               easy_rect.centerx,
               easy_rect.centery,
               window_surface)
    write_text(small_font,
               'Medium',
               settings.BLACK,
               medium_rect.centerx,
               medium_rect.centery,
               window_surface)
    write_text(small_font,
               'Hard',
               settings.BLACK,
               hard_rect.centerx,
               hard_rect.centery,
               window_surface)
    pygame.display.update()
    return easy_rect,medium_rect,hard_rect
    

def get_difficulty(easy_rect,meduim_rect,hard_rect) -> Callable:
    '''根据用户的选择获取电脑要使用的算法'''
    while True:
        for event in pygame.event.get():
            if event.type == pl.QUIT:
                terminate()
            if event.type == pl.KEYUP:
                if event.key == pl.K_ESCAPE:
                    terminate()
            if event.type == pl.MOUSEBUTTONUP:
                x,y = event.pos[0], event.pos[1]
                if easy_rect.collidepoint(x,y):
                    return get_worst_move
                if medium_rect.collidepoint(x,y):
                    return get_random_move
                if hard_rect.collidepoint(x,y):
                    return get_corner_best_move



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
        
        # 监测键鼠事件
        for event in pygame.event.get():
            if event.type == pl.QUIT:
                terminate()

            if event.type == pl.KEYUP:
                if event.key == pl.K_ESCAPE:
                    terminate()
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
                    x,y = event.pos[0],event.pos[1]
                    board.make_move_by_coordinates(x,y)
                    
        
        
        
        
        # 如果轮到电脑出牌，就自动出
        # 电脑没有棋可以下了，就把出牌权交给玩家
        if board.turn == Piece.W:
            if board.get_valid_moves():
                # 电脑的下棋策略是根据玩家选择的难度来选的
                cell = get_computer_move(board)
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

        # 绘制提示，告知用户按M可以开关音乐，按H可以开关提示
        write_text(small_font,
                   'Press M to toggle music',
                   settings.BLACK,
                   window_rect.centerx,
                   480,
                   window_surface)
        write_text(small_font,
                   'Press H to toggle hints',
                   settings.BLACK,
                   window_rect.centerx,
                   510,
                   window_surface)
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
    write_text(big_font,
               word,
               settings.BLACK,
               window_rect.centerx,
               window_rect.centery-50,
               window_surface,
               bg_color
               )    
    # 显示比分
    write_text(small_font,
               f'{player_score} VS {computer_score}',
               settings.BLACK,
               window_rect.centerx,
               window_rect.centery+50,
               window_surface)
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
    # 初始化pygame
    pygame.init()
    main_clock = pygame.time.Clock()
    
    # 设置窗口
    window_surface = pygame.display.set_mode((settings.WINDOW_WIDTH,settings.WINDOW_HEIGHT))
    window_rect = window_surface.get_rect()
    pygame.display.set_caption('翻转棋')

    # 设置大小两种字体
    FONT_PATH = os.path.join(settings.BASE_DIR,'font')
    small_font = pygame.font.Font(os.path.join(FONT_PATH,'msyh.ttf'),24)
    big_font = pygame.font.Font(os.path.join(FONT_PATH,'msyh.ttf'),48)
    

    # 加载音乐文件
    MEDIA_PATH = os.path.join(settings.BASE_DIR,'media')
    pygame.mixer.music.load(os.path.join(MEDIA_PATH,'planB.mp3'))
    win_sound = pygame.mixer.Sound(os.path.join(MEDIA_PATH,'win.wav'))
    tie_sound = pygame.mixer.Sound(os.path.join(MEDIA_PATH,'tie.wav'))
    lose_sound = pygame.mixer.Sound(os.path.join(MEDIA_PATH,'gameover.wav'))
    
    # 只要用户不退出，就还可以一盘接一盘地下
    while True:
        # 游戏开始欢迎画面
        easy_rect, medium_rect, hard_rect = welcome()
        # 等待用户选择难度
        get_computer_move = get_difficulty(easy_rect,medium_rect,hard_rect)
        # 玩一盘，获取最终的得分
        player_score, computer_score = play_game()
        # 根据最终得分显示胜利或者失败的结果
        show_results(player_score,computer_score)
        # 等待用户选择再来一盘或者退出游戏
        if not play_again():
            terminate()

    


        

        
        
    






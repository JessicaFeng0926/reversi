import os

# 文件夹路径
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# 窗口大小
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 600

# 颜色
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)

# 棋子、格子、棋盘大小
PIECE_RADIUS = 22
CELL_SIZE = 50
BOARD_SIZE = CELL_SIZE * 8

# 棋盘左上角坐标
TOP_OF_BOARD = 50
LEFT_OF_BOARD = 50

# 每秒帧数
FPS = 40

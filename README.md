# 黑白翻转棋
一个机遇pygame开发的黑白翻转棋游戏

### 技术栈
python<br/>
pygame <br/>

### 启动方法
1. 双击`reversi.py`文件，在IDLE中启动
2. cd到根目录, 使用指令`python reversi.py`启动
### 目录结构
│  .gitignore<br/>
│  board.py<br/>
│  cell.py<br/>
│  piece.py<br/>
│  README.md<br/>
│  reversi.py<br/>
│  settings.py<br/>
│  strategies.py<br/>
│  
├─font<br/>
│&nbsp;&nbsp;&nbsp;&nbsp;msyh.ttf<br/>
│      
├─media<br/>
│&nbsp;&nbsp;&nbsp;gameover.wav<br/>
│&nbsp;&nbsp;&nbsp;planB.mp3<br/>
│&nbsp;&nbsp;&nbsp;tie.wav<br/>
│&nbsp;&nbsp;&nbsp;win.wav<br/>

### 各目录及文件介绍
***.gitignore:*** 不上传到远程仓库的文件。<br/>
***board.py:*** 这个文件里定义了Board类，也就是棋盘。棋盘是一个容器，包含8行8列共64个Cell对象。初始化的棋盘只有中间四个格子摆放了2颗黑子和2颗白子。Board类只提供了一个对外的属性turn,表示当前的下棋权。Board类提供了一系列方法。change_turn方法把下棋权交给对手；draw_board方法把整个棋盘(包括方法)绘制到屏幕上；is_on_board方法判断鼠标点击的位置是否在棋盘上，返回布尔值；is_valid_row_col方法判断给定的行号和列号是否有效，返回布尔值；is_on_corner方法判断给定的Cell是否在棋盘的角落(棋盘一共有四个角)，返回布尔值；is_full方法判断棋盘是否已经满了，返回布尔值；get_cell_by_coordinates方法根据鼠标的坐标返回鼠标点击的格子，也就是Cell对象；get_cells_to_flip方法判断往给定的格子下棋，能翻转哪些格子的棋子，返回元素是Cell对象的列表；make_move_by_coordinates方法根据坐标下棋，并把出牌权交给对手，这是给玩家用的；make_move_by_cell方法根据Cell对象下棋，并把出牌权交给对手，这是给电脑用的；get_valid_moves方法获取当前状态下，所有能下棋的格子，返回的数据是一个列表，列表里的每个元素是一个元组，元组的第0个元素是Cell对象，第1个元素是把棋子下在这个格子里能翻转的棋子的数量；show_hints方法用于给用户展示提示，也就是在所有能下棋的格子里显示一个整数，这个整数表示如果把棋子下在这个格子里能翻转多少颗棋子；get_score方法返回玩家和电脑的分数，也就是棋盘上黑子和白子的数量。<br/>
***cell.py:*** 在这个文件里定义了一个Cell类，也就是棋盘上的一个格子。这个类也提供了一系列方法。get_rect方法返回这个格子的矩形，也就是一个pygame.Rect对象；set_piece方法把这个格子的棋子更新为传入的Piece对象；draw_piece方法把棋子画在这个格子里；get_piece方法获取这个格子里的棋子，返回一个Piece对象。<br/>
***piece.py:*** 在这个文件里定义了一个Piece类，这个类继承自Enum枚举类。Piece.B表示黑棋，它的值就是大写字母B，Piece.W表示白棋，它的值是大写字母W，Piece.E表示没有棋子，它的值是大写字母E。这个类还有一个只读属性opposite，Piece.B和Piece.W互为opposite,Piece.E的opposite是它本身。<br/>
***reversi.py:*** 这是整个项目的主程序，这里定义了一系列函数，也有游戏的主要逻辑。terminate函数用于关闭游戏；write_text函数用于在平面上写文字，它的参数有字体、要写的文字、颜色、文字的中心x坐标、y坐标、要写文字的平面、背景颜色；welcome函数用于绘制游戏开始界面，这个界面有提示语以及三个不同难度的按钮，这个函数会返回一个元组，元组里有三个难度对应的Rect对象；get_difficulty函数是给用户选择游戏难度的，如果用户点击了关闭按钮或者是按了键盘上的esc按键，那么可以退出游戏，否则就根据用户点击的难度按钮返回相应的策略函数；play_game函数是一局棋的逻辑，它会返回一个元组，里面的两个元素分别是玩家和电脑的分数，这个函数处理的事情出了下棋之外，还包括按M键播放/停止音乐、按H键打开/关闭提示、点击关闭按钮或者按esc键退出游戏，当玩家无处可以下棋或者棋盘满了游戏这局棋就结束；show_results函数根据最终比分在屏幕上显示结果，并且播放对应的音乐；play_again函数是由玩家来决定是否要再下一盘棋，它返回布尔值，点击关闭按钮或者按esc就不下了，其他任意按键都表示要继续。只要用户不结束游戏就可以一盘接一盘地下棋，无限循环就表示棋局可以无限进行下去。我们打开这个程序就会看到欢迎界面，选择了难度之后就可以看到棋盘并且开始下棋了，一局棋结束后能看到比分和结果，我们可以选择继续下棋或者结束游戏。<br/>
***settings.py:*** 存放了这个项目要用的常量。包括根目录的路径，窗口尺寸，几个常用颜色，棋子、格子和棋盘的尺寸，棋盘左上角坐标，每秒帧数。<br/>
***strategies.py:*** 这个文件里定义了三个函数，每个函数都是一种电脑下棋策略，难度不同。get_corner_best_move是难度最高的，这个策略优先抢角，抢不到棋盘的角就选分数最高的位置下棋；get_random_move是中等难度的下棋策略，就是在所有可以下棋的格子中随机选取一个；get_worst_move是最低难度的下棋策略，优先选择非角落的最低分下棋位置，如果只能在角落下棋，那就选角落里的最低分位置。<br/>

        


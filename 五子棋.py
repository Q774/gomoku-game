import pygame
import sys
import numpy as np
from pygame.locals import *

# 初始化pygame
pygame.init()

# 游戏常量
BOARD_SIZE = 15
GRID_SIZE = 40
MARGIN = 50
WINDOW_SIZE = 2 * MARGIN + GRID_SIZE * (BOARD_SIZE - 1)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND = (220, 179, 92)  # 木质棋盘颜色
LINE_COLOR = (0, 0, 0)
HIGHLIGHT = (255, 0, 0)

# 创建游戏窗口
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('五子棋')

# 游戏状态
board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)  # 0: 空, 1: 黑棋, 2: 白棋
current_player = 1  # 1: 黑棋, 2: 白棋
game_over = False
winner = 0
last_move = None

# 字体
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)


def draw_board():
    """绘制棋盘"""
    screen.fill(BACKGROUND)

    # 绘制网格线
    for i in range(BOARD_SIZE):
        # 横线
        pygame.draw.line(screen, LINE_COLOR,
                         (MARGIN, MARGIN + i * GRID_SIZE),
                         (WINDOW_SIZE - MARGIN, MARGIN + i * GRID_SIZE), 2)
        # 竖线
        pygame.draw.line(screen, LINE_COLOR,
                         (MARGIN + i * GRID_SIZE, MARGIN),
                         (MARGIN + i * GRID_SIZE, WINDOW_SIZE - MARGIN), 2)

    # 绘制棋盘上的5个点
    points = [(3, 3), (3, 11), (7, 7), (11, 3), (11, 11)]
    for point in points:
        x, y = point
        pygame.draw.circle(screen, BLACK,
                           (MARGIN + x * GRID_SIZE, MARGIN + y * GRID_SIZE), 5)


def draw_pieces():
    """绘制棋子"""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 1:  # 黑棋
                pygame.draw.circle(screen, BLACK,
                                   (MARGIN + col * GRID_SIZE, MARGIN + row * GRID_SIZE),
                                   GRID_SIZE // 2 - 2)
            elif board[row][col] == 2:  # 白棋
                pygame.draw.circle(screen, WHITE,
                                   (MARGIN + col * GRID_SIZE, MARGIN + row * GRID_SIZE),
                                   GRID_SIZE // 2 - 2)
                pygame.draw.circle(screen, BLACK,
                                   (MARGIN + col * GRID_SIZE, MARGIN + row * GRID_SIZE),
                                   GRID_SIZE // 2 - 2, 1)

    # 绘制最后一步的标记
    if last_move:
        row, col = last_move
        pygame.draw.circle(screen, HIGHLIGHT,
                           (MARGIN + col * GRID_SIZE, MARGIN + row * GRID_SIZE),
                           5)


def draw_info():
    """绘制游戏信息"""
    # 绘制当前玩家信息
    if not game_over:
        player_text = "当前: 黑棋" if current_player == 1 else "当前: 白棋"
        text = font.render(player_text, True, BLACK)
        screen.blit(text, (20, 10))

    # 绘制操作提示
    hint_text = "黑棋: 左键 | 白棋: 右键 | 重置: R"
    hint = small_font.render(hint_text, True, BLACK)
    screen.blit(hint, (WINDOW_SIZE - 250, 10))

    # 绘制游戏结束信息
    if game_over:
        if winner == 1:
            text = font.render("黑棋胜利!", True, BLACK)
        elif winner == 2:
            text = font.render("白棋胜利!", True, BLACK)
        else:
            text = font.render("平局!", True, BLACK)

        # 创建半透明背景
        s = pygame.Surface((WINDOW_SIZE, 60), pygame.SRCALPHA)
        s.fill((255, 255, 255, 180))
        screen.blit(s, (0, WINDOW_SIZE // 2 - 30))

        screen.blit(text, (WINDOW_SIZE // 2 - text.get_width() // 2,
                           WINDOW_SIZE // 2 - text.get_height() // 2))


def check_win(row, col, player):
    """检查是否有玩家获胜"""
    directions = [
        [(0, 1), (0, -1)],  # 水平
        [(1, 0), (-1, 0)],  # 垂直
        [(1, 1), (-1, -1)],  # 对角线
        [(1, -1), (-1, 1)]  # 反对角线
    ]

    for direction_pair in directions:
        count = 1  # 当前位置的棋子

        # 检查两个相反的方向
        for dx, dy in direction_pair:
            temp_row, temp_col = row, col

            # 沿着方向检查连续的棋子
            while True:
                temp_row += dx
                temp_col += dy

                if (0 <= temp_row < BOARD_SIZE and
                        0 <= temp_col < BOARD_SIZE and
                        board[temp_row][temp_col] == player):
                    count += 1
                else:
                    break

            # 如果已经有5个连续的棋子，则获胜
            if count >= 5:
                return True

    return False


def make_move(row, col):
    """在指定位置落子"""
    global board, current_player, game_over, winner, last_move

    # 检查位置是否有效
    if row < 0 or row >= BOARD_SIZE or col < 0 or col >= BOARD_SIZE:
        return False

    # 检查位置是否已有棋子
    if board[row][col] != 0:
        return False

    # 落子
    board[row][col] = current_player
    last_move = (row, col)

    # 检查是否获胜
    if check_win(row, col, current_player):
        game_over = True
        winner = current_player
    # 检查是否平局（棋盘已满）
    elif np.count_nonzero(board) == BOARD_SIZE * BOARD_SIZE:
        game_over = True
        winner = 0
    else:
        # 切换玩家
        current_player = 3 - current_player  # 1->2, 2->1

    return True


def reset_game():
    """重置游戏"""
    global board, current_player, game_over, winner, last_move
    board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    current_player = 1
    game_over = False
    winner = 0
    last_move = None


def main():
    global last_move

    # 主游戏循环
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # 鼠标点击事件
            if event.type == MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos

                # 计算棋盘位置
                col = round((x - MARGIN) / GRID_SIZE)
                row = round((y - MARGIN) / GRID_SIZE)

                # 检查点击是否在棋盘范围内
                if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                    # 左键: 黑棋
                    if event.button == 1 and current_player == 1:
                        make_move(row, col)
                    # 右键: 白棋
                    elif event.button == 3 and current_player == 2:
                        make_move(row, col)

            # 键盘事件
            if event.type == KEYDOWN:
                if event.key == K_r:  # 按R重置游戏
                    reset_game()
                elif event.key == K_ESCAPE:  # 按ESC退出
                    pygame.quit()
                    sys.exit()

        # 绘制游戏
        draw_board()
        draw_pieces()
        draw_info()

        pygame.display.flip()


if __name__ == "__main__":
    main()
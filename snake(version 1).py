import pygame
import time
import random

pygame.init()

# some useful color
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
yellow = (255, 255, 102)
green = (0, 255, 0)
blue = (50, 153, 213)
purple = (255, 0, 255)
grey = (150, 150, 150)


# 遊戲視窗
dis_width = 640
dis_height = 480
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("THE SNAKE")

# 時間
clock = pygame.time.Clock()

# 字體
def font(size, Type = "SIMYOU.TTF"):
    return pygame.font.SysFont(Type, size)
basic_font = font(20)

# 蛇
snake_block = 16
snake_speed = 20
def draw_snake(snake_body, snake_block):
    for i in snake_body:
        pygame.draw.rect(dis, blue, [i[0], i[1], snake_block, snake_block])

# 得分
def draw_score(score):
    value = basic_font.render("Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])

# 宣布
def message(msg, color):
    mesg = basic_font.render(msg, True, color)
    dis.blit(mesg, [dis_width / 2 - len(msg) * 3, dis_height / 2])


# 主程式
def gameLoop():
    game_over = False
    game_close = False
    last = "RIGHT"
    
    # 蛇起始
    snake_len = 3
    snake_body = []
    for i in range(snake_len):
        snake_body.append([0 + i * snake_block, dis_height / 2])
    x_change = 0
    y_change = 0
    
    # 蘋果起始
    x_apple = int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block
    y_apple = int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block
    
    # 遊戲中
    while not game_over:
        #控制遊戲速度
        clock.tick(snake_speed)
        
        # 輸遊戲後 SPACE則繼續 ESC則關閉遊戲
        while game_close == True:
            dis.fill(black)
            message(f"You Lost! Your snake ate {snake_len - 3} apples! Press 'space'--play again or 'esc'--quit", red)
            draw_score(snake_len - 3)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_SPACE:
                        gameLoop()
        
        # 判斷遊戲是否結束 & 上下左右
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                
            # 按按鍵時
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and last != "RIGHT":
                    x_change = -snake_block
                    y_change = 0
                    last = "LEFT"
                elif event.key == pygame.K_RIGHT and last != "LEFT":
                    x_change = snake_block
                    y_change = 0
                    last = "RIGHT"
                elif event.key == pygame.K_UP and last != "DOWN":
                    x_change = 0
                    y_change = -snake_block
                    last = "UP"
                elif event.key == pygame.K_DOWN and last != "UP":
                    x_change = 0
                    y_change = snake_block
                    last = "DOWN"
        
        # 紀錄蛇頭位置
        x_head, y_head = snake_body[-1][0], snake_body[-1][1]
        
        # 蛇撞牆
        if not (0 <= x_head <= dis_width - snake_block * 0.5 and 0 <= y_head <= dis_height - snake_block * 0.5):
            game_close = True
            
        # 背景 & 蘋果
        dis.fill(black)
        pygame.draw.rect(dis, red, [x_apple, y_apple, int(snake_block / 2), int(snake_block / 2)])
            
        # 記錄蛇 長度 & 位置
        if not x_change == y_change == 0:
            x_head += x_change
            y_head += y_change
            snake_body.append([x_head, y_head])
        if len(snake_body) > snake_len:
            del snake_body[0]
        
        # 蛇撞身體
        for j in snake_body[:-1]:
            if j == [x_head, y_head]:
                game_close = True
        
         # 劃出 蛇 & 分數
        draw_snake(snake_body, snake_block)
        draw_score(snake_len - 3)
        
        pygame.display.update()
        
        # 吃到蘋果
        if x_head == x_apple and y_head == y_apple:
            while [x_apple, y_apple] in snake_body:
                x_apple = int(random.randint(0, dis_width) / snake_block) * snake_block
                y_apple = int(random.randint(0, dis_height) / snake_block) * snake_block
            snake_len += 1
 
    pygame.quit()
    quit()
  
 
gameLoop()

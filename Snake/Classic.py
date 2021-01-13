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
indigo = (0, 0, 255)
purple = (255, 0, 255)
grey = (150, 150, 150)
orange = (255,165,0)

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
disp_font = font(25)
basic_font = font(30)

# 蛇
snake_block = 16
snake_speed = 15
def draw_snake(snake_body, snake_block):
    for i in snake_body:
        pygame.draw.rect(dis, blue, [i[0], i[1], snake_block, snake_block])

# 得分
def draw_score(score):
    value = disp_font.render("Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])

# 宣布
def message(msg, color):
    mesg = basic_font.render(msg, True, color)
    dis.blit(mesg, [dis_width / 2 - len(msg) * 5, dis_height / 2])
    
def random_move(X,Y):
    opt = random.randint(0,3)
    if(opt==0):
        if(X==dis_width-snake_block):
            if(Y==0 or Y==dis_height-snake_block):
                random_move(X,Y)
        else:
            X+=snake_block
    elif(opt==1):
        if(X==0):
            if(Y==0 or Y==dis_height-snake_block):
                random_move(X,Y)
        else:
            X-=snake_block
    elif(opt==2):
        if(Y==dis_width-snake_block):
            if(X==0 or X==dis_width-snake_block):
                random_move(X,Y)
        else:
            Y-=snake_block
    else:
        if(Y==0):
            if(X==0 or X==dis_width-snake_block):
                random_move(X,Y)
        else:
            Y+=snake_block
    return (X,Y)

# 主程式
def gameLoop():
    game_over = False
    game_close = False
    game_start = False
    last = "RIGHT"
    backgroungImg = pygame.image.load('grid.png')

    # 蛇起始
    snake_len = 3
    snake_body = []
    for i in range(snake_len):
        snake_body.append([0 + i * snake_block, dis_height / 2])
    x_change = 0
    y_change = 0

    # 蘋果起始
    Qa = 5
    x_apple = [int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block for _ in range(Qa)]
    y_apple = [int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block for _ in range(Qa)]
    appleImg = pygame.image.load('apple.png')
    
    # 炸彈起始
    Qe = 3
    bombImg = pygame.image.load('bomb.png')
    x_bomb = [int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block for _ in range(Qe)]
    y_bomb = [int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block for _ in range(Qe)]
    time = 30
    countdown = snake_speed* time
    movecycle, lurkcycle, bananacycle = 0, 0, 0
    item_move = 5
    bomb_lurk = 3
    banana_lurk = 1
    
    # 遊戲中
    while not game_over:
        if countdown==0:
            game_close = True
        elif countdown >= snake_speed* time:
            countdown = snake_speed* time
        
        #控制遊戲速度
        clock.tick(snake_speed)
        
        # 輸遊戲後 SPACE則繼續 ESC則關閉遊戲
        while game_close == True:
            dis.fill(black)
            message(f"GAME OVER! Your final score is {snake_len - 3}.", red)
            
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
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT):
                game_start = True
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
        if (x_head < 0 or x_head > dis_width-snake_block or y_head < 0 or y_head > dis_height-snake_block):
            game_close = True
            
        # 背景 & 道具
        dis.blit(backgroungImg, (0,0))
        for i1 in range(Qa):
            dis.blit(appleImg, (x_apple[i1], y_apple[i1]))
        for i2 in range(Qe):
            dis.blit(bombImg, (x_bomb[i2], y_bomb[i2]))
        
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
        
        # 劃出 蛇 & 分數 & 時間
        draw_snake(snake_body, snake_block)
        draw_score(snake_len - 3)
        pygame.display.update()

        # 吃到蘋果
        for k1 in range(Qa):
            if x_head == x_apple[k1] and y_head == y_apple[k1]:
                while [x_apple[k1], y_apple[k1]] in snake_body:
                    x_apple[k1] = int(random.randint(0, dis_width) / snake_block) * snake_block
                    y_apple[k1] = int(random.randint(0, dis_height) / snake_block) * snake_block
                snake_len += 1

        # 吃到炸彈
        for k2 in range(Qe):
            if x_head == x_bomb[k2] and y_head == y_bomb[k2]:
                game_close = True

    pygame.quit()
    quit()
  
 
gameLoop()

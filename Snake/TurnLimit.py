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
basic_font = font(25)
ann_font = font(30)

# 蛇
snake_block = 16
snake_speed = 10
def draw_snake(snake_body, snake_block):
    for i in snake_body:
        pygame.draw.rect(dis, blue, [i[0], i[1], snake_block, snake_block])

# 得分
def draw_score(score):
    value = basic_font.render("Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])

#轉向
def draw_turns(turn):
    value = basic_font.render(f'Left Turns: {turn}', True, blue)
    dis.blit(value, [0, 20])

# 宣布
def message(msg, color):
    mesg = ann_font.render(msg, True, color)
    dis.blit(mesg, [dis_width / 2 - len(msg) * 5, dis_height / 2])

# 主程式
def gameLoop():
    game_over = False
    game_close = False
    last = "RIGHT"
    background = pygame.image.load('./grid.png')
    score = 0
    bomb_count = 1
    banana_count = 1
    orange_count = 1
    
    # 蛇起始
    snake_len = 3
    snake_body = []
    for i in range(snake_len):
        snake_body.append([0 + i * snake_block, dis_height / 2])
    x_change = 0
    y_change = 0


    #牆起始
    walls = []
    for i in range(15):
        walls.append([random.randint(0,dis_width/snake_block)*snake_block,random.randint(0,dis_height/snake_block)*snake_block])
            
    # 蘋果起始
    apples = []
    x_apples = []
    y_apples = []
    for i in range(3):
        apple = pygame.image.load('./apple.png')
        x_apple = int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block
        y_apple = int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block
        apples.append(apple)
        x_apples.append(x_apple)
        y_apples.append(y_apple)

    #香蕉起始
    banana = pygame.image.load('./banana.png')
    x_banana = int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block
    y_banana = int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block
    
    #橘子起始
    orange = pygame.image.load('./orange.png')
    x_orange = int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block
    y_orange = int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block

    #炸彈起始
    bombs = []
    x_bombs = []
    y_bombs = []
    for i in range(3):
        bomb = pygame.image.load('./bomb.png')
        x_bomb = int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block
        y_bomb = int(random.randint(0, dis_height - snake_block) / snake_block)* snake_block
        bombs.append(bomb)
        x_bombs.append(x_bomb)
        y_bombs.append(y_bomb)

    #起始轉數
    turn = 6

    # 遊戲中
    while not game_over:
        #控制遊戲速度
        clock.tick(snake_speed)
        
        # 輸遊戲後 SPACE則繼續 ESC則關閉遊戲
        while game_close == True:
            dis.fill(black)
            message(f"GAME OVER! You got {score} scores!", red)
            draw_score(score)
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
                bomb_count += 1
                orange_count += 1
                banana_count += 1
                if event.key == pygame.K_LEFT and last != "RIGHT":
                    x_change = -snake_block
                    y_change = 0
                    last = "LEFT"
                    turn -= 1
                elif event.key == pygame.K_RIGHT and last != "LEFT":
                    x_change = snake_block
                    y_change = 0
                    last = "RIGHT"
                    turn -= 1
                elif event.key == pygame.K_UP and last != "DOWN":
                    x_change = 0
                    y_change = -snake_block
                    last = "UP"
                    turn -= 1
                elif event.key == pygame.K_DOWN and last != "UP":
                    x_change = 0
                    y_change = snake_block
                    last = "DOWN"
                    turn -=1
        
        # 紀錄蛇頭位置
        x_head, y_head = snake_body[-1][0], snake_body[-1][1]
        
        # 蛇撞牆
        if not (0 <= x_head <= dis_width - snake_block * 0.5 and 0 <= y_head <= dis_height - snake_block * 0.5):
            game_close = True
        for i in range(len(walls)):
            if x_head == walls[i][0] and y_head == walls[i][1]:
                game_close = True

        # 背景 & 果實
        dis.blit(background, (0,0))
        for i in range(3):
            dis.blit(apples[i], (x_apples[i], y_apples[i]))
            dis.blit(bombs[i], (x_bombs[i], y_bombs[i]))
        dis.blit(banana, (x_banana, y_banana))
        dis.blit(orange, (x_orange, y_orange))

        #畫牆
        for i in range(len(walls)):
            pygame.draw.rect(dis, green, [walls[i][0], walls[i][1], int(snake_block), int(snake_block)])

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

        #轉數用完
        if turn == -1:
            game_close = True
        
        # 畫出 蛇 & 分數 & 轉數
        draw_snake(snake_body, snake_block)
        draw_score(score)
        draw_turns(turn)
        
        pygame.display.update()
        
        # 吃到蘋果
        for i in range(3):
            if x_head == x_apples[i] and y_head == y_apples[i]:
                while [x_apples[i], y_apples[i]] in snake_body or  [x_apple, y_apple] in walls:
                    x_apples[i] = int(random.randint(0, dis_width) / snake_block) * snake_block
                    y_apples[i] = int(random.randint(0, dis_height) / snake_block) * snake_block
                snake_len += 1
                turn += 4
                score += 1

        #吃到橘子
        if x_head == x_orange and y_head == y_orange :
            while [x_orange, y_orange] in snake_body or [x_orange, y_orange] in walls:
                x_orange = int(random.randint(0, dis_width) / snake_block) * snake_block
                y_orange = int(random.randint(0, dis_height) / snake_block) * snake_block
            snake_len += 1
            score += 3
            turn += 2
            
        # 吃到炸彈
        for i in range(3):
            if x_head == x_bombs[i] and y_head == y_bombs[i]:
                game_close = True

        # 吃到香蕉
        if x_head == x_banana and y_head == y_banana or [x_banana, y_banana] in walls:
            while [x_banana, y_banana] in snake_body:
                x_banana = int(random.randint(0, dis_width) / snake_block) * snake_block
                y_banana = int(random.randint(0, dis_height) / snake_block) * snake_block
            turn += 7

        #更新果實位置
        if  bomb_count % (5) == 0:
            for i in range(3):
                x_bombs[i] = int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block
                y_bombs[i] = int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block
            while [x_bomb, y_bomb] in walls:
                x_bomb = int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block
                y_bomb = int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block
            bomb_count += 1
        if  banana_count % (4) == 0:
            x_banana = int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block
            y_banana = int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block
            while [x_banana, y_banana] in walls:
                x_banana = int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block
                y_banana = int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block
            banana_count += 1
        if  orange_count % (3) == 0:
            move = random.randint(1,4)
            if move == 1:
                x_orange += 1 * snake_block
            if move == 2:
                x_orange -= 1 * snake_block
            if move == 3:
                y_orange += 1 * snake_block
            if move == 4:
                y_orange -= 1 * snake_block
            while [x_orange, y_orange] in walls:
                if move == 1:
                    x_orange += 1 * snake_block
                if move == 2:
                    x_orange -= 1 * snake_block
                if move == 3:
                    y_orange += 1 * snake_block
                if move == 4:
                    y_orange -= 1 * snake_block
            orange_count += 1
 
    pygame.quit()
    quit()
  
 
gameLoop()

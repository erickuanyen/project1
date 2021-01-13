import pygame
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

# 蛇（玩家＆電腦）

snake_block = 16
snake_speed = 12
def draw_player(snake_body, snake_block):
    for i in snake_body:
        pygame.draw.rect(dis, indigo, [i[0], i[1], snake_block, snake_block])
def draw_AI(snake_body, snake_block):
    for i in snake_body:
        pygame.draw.rect(dis, white, [i[0], i[1], snake_block, snake_block])

# 宣布
def message(msg, font, color, pos):
    mesg = font.render(msg, True, color)
    dis.blit(mesg, pos)

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
    last_AI1 = "RIGHT"
    last_AI2 = last_AI1
    life1 = 1
    life2 = 1
    life1_ = 0
    life2_ = 0
    backgroungImg = pygame.image.load('grid.png')
    
    # player起始
    player_len = 3
    player_body = []
    for i in range(player_len):
        player_body.append([0 + i * snake_block, dis_height / 3])
    x1_change = 0
    y1_change = 0
    
    # AI起始
    AI_len = 3
    AI_body = []
    for i in range(AI_len):
        AI_body.append([0 + i * snake_block, 2*dis_height / 3])
    x2_change = 0
    y2_change = 0
    hit_self = False
    
    # 蘋果起始
    Qa = 3
    x_apple = [int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block for _ in range(Qa)]
    y_apple = [int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block for _ in range(Qa)]
    appleImg = pygame.image.load('apple.png')
    target = random.randint(0, Qa - 1)
    
    # 炸彈起始
    Qe = 10
    bombImg = pygame.image.load('bomb.png')
    x_bomb = [int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block for _ in range(Qe)]
    y_bomb = [int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block for _ in range(Qe)]
    player_bombtouch, AI_bombtouch = 0, 0
    player_walltouch, AI_walltouch = 0, 0
    player_selftouch, AI_selftouch = 0, 0
    
    # 遊戲中
    while not game_over:
            
        #控制遊戲速度
        clock.tick(snake_speed)
        
        # 輸遊戲後 SPACE則繼續 ESC則關閉遊戲
        while game_close == True:
            dis.fill(black)
            if player_bombtouch == 1 or player_walltouch == 1 or player_selftouch == 1:
                message("GAME OVER. The AI wins!", font(30), red, [dis_width / 2 - 115, dis_height / 2])
            elif AI_bombtouch == 1 or AI_walltouch == 1 or AI_selftouch == 1:
                message("GAME OVER. You win!", font(30), red, [dis_width / 2 - 95, dis_height / 2])
                
            #draw_score(snake_len - 3)
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
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                game_start = True
                if event.key == pygame.K_LEFT and last != "RIGHT":
                    x1_change = -snake_block
                    y1_change = 0
                    last = "LEFT"
                elif event.key == pygame.K_RIGHT and last != "LEFT":
                    x1_change = snake_block
                    y1_change = 0
                    last = "RIGHT"
                elif event.key == pygame.K_UP and last != "DOWN":
                    x1_change = 0
                    y1_change = -snake_block
                    last = "UP"
                elif event.key == pygame.K_DOWN and last != "UP":
                    x1_change = 0
                    y1_change = snake_block
                    last = "DOWN"
        
        # 紀錄蛇頭位置
        x1_head, y1_head = player_body[-1][0], player_body[-1][1]
        x2_head, y2_head = AI_body[-1][0], AI_body[-1][1]
        
        # AI
        if game_start:
            last_AI2 = last_AI1
            if x_apple[target] < x2_head:
                if last_AI1 != "RIGHT":
                    x2_change = -snake_block
                    y2_change = 0
                    last_AI1 = "LEFT"
                else:
                    if y_apple[target] < y2_head:
                        x2_change = 0
                        y2_change = -snake_block
                        last_AI1 = "UP"
                    else:
                        x2_change = 0
                        y2_change = snake_block
                        last_AI1 = "DOWN"
            elif x_apple[target] > x2_head:
                if last_AI1 != "LEFT":
                    x2_change = snake_block
                    y2_change = 0
                    last_AI1 = "RIGHT"
                else:
                    if y_apple[target] < y2_head:
                        x2_change = 0
                        y2_change = -snake_block
                        last_AI1 = "UP"
                    else:
                        x2_change = 0
                        y2_change = snake_block
                        last_AI1 = "DOWN"
            else:
                if y_apple[target] < y2_head:
                    if last_AI1 != "DOWN":
                        x2_change = 0
                        y2_change = -snake_block
                        last_AI1 = "UP"
                    else:
                        x2_change = snake_block
                        y2_change = 0
                        last_AI1 = "RIGHT"
                else:
                    if last_AI1 != "UP":
                        x2_change = 0
                        y2_change = snake_block
                        last_AI1 = "DOWN"
                    else:
                        x2_change = snake_block
                        y2_change = 0
                        last_AI1 = "RIGHT"
                    
        # 蛇撞牆
        if x1_head < 0 or x1_head > dis_width-snake_block or y1_head < 0 or y1_head > dis_height-snake_block:
            player_walltouch = 1
            game_close = True
        if x2_head < 0 or x2_head > dis_width-snake_block or y2_head < 0 or y2_head > dis_height-snake_block:
            AI_walltouch = 1
            game_close = True
        
         # AI遇 bump & wall & 身體時 (95%機率轉向)
        for i in range(Qe):
            if (x2_head+x2_change == x_bomb[i] and y2_head+y2_change == y_bomb[i]) and random.random() <= 0.95:
                if last_AI1 == last_AI2:
                    direction = last_AI1
                else:
                    direction = last_AI2
                if direction in ("RIGHT", "LEFT"):
                    if y_apple[target] < y2_head:
                        x2_change = 0
                        y2_change = -snake_block
                        last_AI1 == "UP"
                    else:
                        x2_change = 0
                        y2_change = snake_block
                        last_AI1 = "DOWN"
                else:
                    if x_apple[target] < x2_head:
                        x2_change = -snake_block
                        y2_change = 0
                        last_AI1 = "LEFT"
                    else:
                        x2_change = snake_block
                        y2_change = 0
                        last_AI1 = "RIGHT"
        if not (0<=x2_head+x2_change<=dis_width and 0<=y2_head+y2_change<=dis_width) and random.random()<=0.95:
            if last_AI1 in ("RIGHT", "LEFT"):
                if y_apple[target] < y2_head:
                    x2_change = 0
                    y2_change = -snake_block
                    last_AI1 == "UP"
                else:
                    x2_change = 0
                    y2_change = snake_block
                    last_AI1 = "DOWN"
            else:
                if x_apple[target] < x2_head:
                    x2_change = -snake_block
                    y2_change = 0
                    last_AI1 = "LEFT"
                else:
                    x2_change = snake_block
                    y2_change = 0
                    last_AI1 = "RIGHT"
            
        # 背景 & 道具
        dis.blit(backgroungImg, (0,0))
        for i1 in range(Qa):
            dis.blit(appleImg, (x_apple[i1], y_apple[i1]))
        for i2 in range(Qe):
            dis.blit(bombImg, (x_bomb[i2], y_bomb[i2]))
        
        # 記錄蛇 長度 & 位置
        message(f"Player's Life: {life1}   ({life1_}/10)", font(20), yellow, [0, 0])
        message(f"AI's Life: {life2}   ({life2_}/10)", font(20), yellow, [0, 15])
        if not x1_change == y1_change == 0:
            x1_head += x1_change
            y1_head += y1_change
            player_body.append([x1_head, y1_head])
        if len(player_body) > player_len:
            player_tail = player_body[0] 
            del player_body[0]
            
        if not x2_change == y2_change == 0:
            x2_head += x2_change
            y2_head += y2_change
            AI_body.append([x2_head, y2_head])
        if len(AI_body) > AI_len:
            AI_tail = AI_body[0]
            del AI_body[0]
        
        # 蛇撞身體
        for j in player_body[:-1]:
            if j == [x1_head, y1_head]:
                life1 -= 1
                if life1 == 0:
                    player_selftouch = 1
                    game_close = True
                
        if j in AI_body[:-1]:
            if j == [x2_head, y2_head]:
                print("yes")
                life2 -= 1
                if life2 == 0:
                    AI_selftouch = 1
                    game_close = True

        # 劃出 蛇 & 分數 & 時間
        draw_AI(AI_body, snake_block)
        draw_player(player_body, snake_block)
        pygame.display.update()
        
        # 吃到蘋果
        for k1 in range(Qa):
            if x1_head == x_apple[k1] and y1_head == y_apple[k1]:
                AI_body.insert(0, AI_tail)
                AI_len += 1
                life1_ += 1
                while [x_apple[k1], y_apple[k1]] in player_body or [x_apple[k1], y_apple[k1]] in AI_body:
                    x_apple[k1] = int(random.randint(0, dis_width) / snake_block) * snake_block
                    y_apple[k1] = int(random.randint(0, dis_height) / snake_block) * snake_block
            if x2_head == x_apple[k1] and y2_head == y_apple[k1]:
                player_tail.insert(0, player_tail)
                player_len += 1
                life2_ += 1
                target = random.randint(0, Qa - 1)
                while [x_apple[k1], y_apple[k1]] in player_body or [x_apple[k1], y_apple[k1]] in AI_body:
                    x_apple[k1] = int(random.randint(0, dis_width) / snake_block) * snake_block
                    y_apple[k1] = int(random.randint(0, dis_height) / snake_block) * snake_block
        if life1_ == 10:
            life1 += 1
            life1_ = 0
        if life2_ == 10:
            life2 += 1
            life2_ = 0
                
        # 吃到炸彈
        for k2 in range(Qe):
            if x1_head == x_bomb[k2] and y1_head == y_bomb[k2]:
                life1 -= 1
                while [x_bomb[k2], y_bomb[k2]] in player_body or [x_bomb[k2], y_bomb[k2]] in AI_body:
                    x_bomb[k2] = int(random.randint(0, dis_width) / snake_block) * snake_block
                    y_bomb[k2] = int(random.randint(0, dis_height) / snake_block) * snake_block
                if life1 == 0:
                    player_bombtouch = 1
                    game_close = True
            if x2_head == x_bomb[k2] and y2_head == y_bomb[k2]:
                life2 -= 1
                while [x_bomb[k2], y_bomb[k2]] in player_body or [x_bomb[k2], y_bomb[k2]] in AI_body:
                    x_bomb[k2] = int(random.randint(0, dis_width) / snake_block) * snake_block
                    y_bomb[k2] = int(random.randint(0, dis_height) / snake_block) * snake_block
                if life2 == 0:
                    AI_bombtouch = 1
                    game_close = True
            
    pygame.quit()
    quit()
  
 
gameLoop()

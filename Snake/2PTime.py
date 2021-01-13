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
basic_font = font(20)
ann_font = font(30)

# 蛇1,2
snake_block = 16
snake_speed = 10
def draw_snake1(snake_body, snake_block):
    for i in snake_body:
        pygame.draw.rect(dis, indigo, [i[0], i[1], snake_block, snake_block])
def draw_snake2(snake_body, snake_block):
    for i in snake_body:
        pygame.draw.rect(dis, white, [i[0], i[1], snake_block, snake_block])

# 計時
def draw_timer1(timer):
    value = disp_font.render("Timer01: " + str(timer//snake_speed), True, green)
    dis.blit(value, [0, 0])
def draw_timer2(timer):
    value = disp_font.render("Timer02: " + str(timer//snake_speed), True, green)
    dis.blit(value, [0, 20])

# 宣布
def message(msg, color):
    mesg = ann_font.render(msg, True, color)
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
    last1 = "RIGHT1"
    last2 = "RIGHT2"
    backgroungImg = pygame.image.load('grid.png')

    # 蛇1起始
    snake1_len = 3
    snake1_body = []
    for i in range(snake1_len):
        snake1_body.append([0 + i * snake_block, dis_height / 3])
    x1_change = 0
    y1_change = 0
    
    # 蛇2起始
    snake2_len = 3
    snake2_body = []
    for i in range(snake2_len):
        snake2_body.append([0 + i * snake_block, 2*dis_height / 3])
    x2_change = 0
    y2_change = 0
    
    # 蘋果起始
    Qa = 5
    x_apple = [int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block for _ in range(Qa)]
    y_apple = [int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block for _ in range(Qa)]
    appleImg = pygame.image.load('apple.png')
    
    # 香蕉起始
    Qb = 2
    bananaImg = pygame.image.load('banana.png')
    x_banana = [int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block for _ in range(Qb)]
    y_banana = [int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block for _ in range(Qb)]
    
    # 橘子起始
    Qo = 3
    orangeImg = pygame.image.load('orange.png')
    x_orange = [int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block for _ in range(Qo)]
    y_orange = [int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block for _ in range(Qo)]
    
    # 炸彈起始
    Qe = 5
    bombImg = pygame.image.load('bomb.png')
    x_bomb = [int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block for _ in range(Qe)]
    y_bomb = [int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block for _ in range(Qe)]
    time = 15
    countdown1 = snake_speed* time
    countdown2 = snake_speed* time
    movecycle, lurkcycle, bananacycle = 0, 0, 0
    item_move = 5
    bomb_lurk = 5
    banana_lurk = 1
    p1timeup, p2timeup, p1bombtouch, p2bombtouch, p1walltouch, p2walltouch, p1selftouch, p2selftouch= 0, 0, 0, 0, 0, 0, 0, 0
    # 遊戲中
    while not game_over:
        if countdown1==0:
            game_close = True
            p1timeup = 1
        elif countdown2==0:
            game_close = True
            p2timeup = 1
        elif countdown1 >= snake_speed* time:
            countdown1 = snake_speed* time
        elif countdown2 >= snake_speed* time:
            countdown2 = snake_speed* time
            
        #控制遊戲速度
        clock.tick(snake_speed)
        
        # 輸遊戲後 SPACE則繼續 ESC則關閉遊戲
        while game_close == True:
            dis.fill(black)
            if p1timeup == 1 or p1bombtouch == 1 or p1walltouch==1 or p1selftouch==1:
                message(f"GAME OVER. Player 1 is killed. Player 2 wins!", red)
            elif p2timeup==1 or p2bombtouch == 1 or p2walltouch==1 or p2selftouch==1:
                message(f"GAME OVER. Player 2 is killed. Player 1 wins!", red)
                
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

        # 按按鍵時P1
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT):
                game_start = True
                if event.key == pygame.K_LEFT and last1 != "RIGHT1":
                    x1_change = -snake_block
                    y1_change = 0
                    last1 = "LEFT1"
                elif event.key == pygame.K_RIGHT and last1 != "LEFT1":
                    x1_change = snake_block
                    y1_change = 0
                    last1 = "RIGHT1"
                elif event.key == pygame.K_UP and last1 != "DOWN1":
                    x1_change = 0
                    y1_change = -snake_block
                    last1 = "UP1"
                elif event.key == pygame.K_DOWN and last1 != "UP1":
                    x1_change = 0
                    y1_change = snake_block
                    last1 = "DOWN1"
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_a, pygame.K_w, pygame.K_s, pygame.K_d):
                game_start = True
                if event.key == pygame.K_a and last2 != "RIGHT2":
                    x2_change = -snake_block
                    y2_change = 0
                    last2 = "LEFT2"
                elif event.key == pygame.K_d and last2 != "LEFT2":
                    x2_change = snake_block
                    y2_change = 0
                    last2 = "RIGHT2"
                elif event.key == pygame.K_w and last2 != "DOWN2":
                    x2_change = 0
                    y2_change = -snake_block
                    last2 = "UP2"
                elif event.key == pygame.K_s and last2 != "UP2":
                    x2_change = 0
                    y2_change = snake_block
                    last2 = "DOWN2"
                    
        # 紀錄蛇頭位置
        x1_head, y1_head = snake1_body[-1][0], snake1_body[-1][1]
        x2_head, y2_head = snake2_body[-1][0], snake2_body[-1][1]
        
        # 蛇撞牆
        if (x1_head < 0 or x1_head > dis_width-snake_block or y1_head < 0 or y1_head > dis_height-snake_block):
            p1walltouch = 1
            game_close = True
        if (x2_head < 0 or x2_head > dis_width-snake_block or y2_head < 0 or y2_head > dis_height-snake_block):
            p2walltouch = 1
            game_close = True
            
        # 背景 & 道具
        dis.blit(backgroungImg, (0,0))
        for i1 in range(Qa):
            dis.blit(appleImg, (x_apple[i1], y_apple[i1]))
        for i2 in range(Qe):
            dis.blit(bombImg, (x_bomb[i2], y_bomb[i2]))
        for i3 in range(Qb):
            dis.blit(bananaImg, (x_banana[i3], y_banana[i3]))
        for i4 in range(Qo):
            dis.blit(orangeImg, (x_orange[i4], y_orange[i4]))
        
        # 記錄蛇 長度 & 位置
        if not x1_change == y1_change == 0:
            x1_head += x1_change
            y1_head += y1_change
            snake1_body.append([x1_head, y1_head])
        if len(snake1_body) > snake1_len:
            del snake1_body[0]
            
        if not x2_change == y2_change == 0:
            x2_head += x2_change
            y2_head += y2_change
            snake2_body.append([x2_head, y2_head])
        if len(snake2_body) > snake2_len:
            del snake2_body[0]
        
        # 蛇撞身體
        for j in snake1_body[:-1]:
            if j == [x1_head, y1_head]:
                p1selftouch = 1
                game_close = True
                
        for j in snake2_body[:-1]:
            if j == [x2_head, y2_head]:
                p2selftouch = 1
                game_close = True
        
        # 劃出 蛇 & 分數 & 時間
        draw_snake1(snake1_body, snake_block)
        draw_snake2(snake2_body, snake_block)
        draw_timer1(countdown1)
        draw_timer2(countdown2)
        pygame.display.update()
        
        # 吃到蘋果
        for k1 in range(Qa):
            if x1_head == x_apple[k1] and y1_head == y_apple[k1]:
                while [x_apple[k1], y_apple[k1]] in snake1_body:
                    x_apple[k1] = int(random.randint(0, dis_width) / snake_block) * snake_block
                    y_apple[k1] = int(random.randint(0, dis_height) / snake_block) * snake_block
                snake1_len += 1
            if x2_head == x_apple[k1] and y2_head == y_apple[k1]:
                while [x_apple[k1], y_apple[k1]] in snake2_body:
                    x_apple[k1] = int(random.randint(0, dis_width) / snake_block) * snake_block
                    y_apple[k1] = int(random.randint(0, dis_height) / snake_block) * snake_block
                snake2_len += 1
                
        # 吃到香蕉
        for k2 in range(Qb):
            if x1_head == x_banana[k2] and y1_head == y_banana[k2]:
                while [x_banana[k2], y_banana[k2]] in snake1_body:
                    x_banana[k2] = int(random.randint(0, dis_width) / snake_block) * snake_block
                    y_banana[k2] = int(random.randint(0, dis_height) / snake_block) * snake_block
                snake1_len += 5
            if x2_head == x_banana[k2] and y2_head == y_banana[k2]:
                while [x_banana[k2], y_banana[k2]] in snake2_body:
                    x_banana[k2] = int(random.randint(0, dis_width) / snake_block) * snake_block
                    y_banana[k2] = int(random.randint(0, dis_height) / snake_block) * snake_block
                snake2_len += 5  
                
        # 吃到橘子
        for k3 in range(Qo):
            if x1_head == x_orange[k3] and y1_head == y_orange[k3]:
                while [x_orange[k3], y_orange[k3]] in snake1_body:
                    x_orange[k3] = int(random.randint(0, dis_width) / snake_block) * snake_block
                    y_orange[k3] = int(random.randint(0, dis_height) / snake_block) * snake_block
                countdown1+=random.randint(1, 5)*snake_speed
            if x2_head == x_orange[k3] and y2_head == y_orange[k3]:
                while [x_orange[k3], y_orange[k3]] in snake2_body:
                    x_orange[k3] = int(random.randint(0, dis_width) / snake_block) * snake_block
                    y_orange[k3] = int(random.randint(0, dis_height) / snake_block) * snake_block
                countdown2+=random.randint(1, 5)*snake_speed
                
        # 吃到炸彈
        for k4 in range(Qe):
            if x1_head == x_bomb[k4] and y1_head == y_bomb[k4]:
                p1bombtouch = 1
                game_close = True
            if x2_head == x_bomb[k4] and y2_head == y_bomb[k4]:
                p2bombtouch = 1
                game_close = True
            
        # 時間循環要移動
        if game_start ==True:
            countdown1-=1
            countdown2-=1
            if(movecycle%(item_move*snake_speed) == 0 and movecycle!=0):
                for j1 in range(Qa):
                    newA = random_move(x_apple[j1],y_apple[j1])
                    (x_apple[j1],y_apple[j1]) = newA
                for j2 in range(Qo):
                    newO = random_move(x_orange[j2],y_orange[j2])
                    (x_orange[j2],y_orange[j2]) = newO
                movecycle=0
            else:
                movecycle+=1
            if(bananacycle%(banana_lurk*snake_speed) == 0 and bananacycle!=0):
                for l1 in range(Qb):
                    x_banana[l1] = int(random.randint(0, dis_width) / snake_block) * snake_block
                    y_banana[l1] = int(random.randint(0, dis_height) / snake_block) * snake_block
                    bananacycle=0
            else:
                bananacycle+=1
            
            if(lurkcycle%(bomb_lurk*snake_speed) == 0 and lurkcycle!=0):
                for m1 in range(Qe):
                    x_bomb[m1] = int(random.randint(0, dis_width) / snake_block) * snake_block
                    y_bomb[m1] = int(random.randint(0, dis_height) / snake_block) * snake_block
                    lurkcycle=0
            else:
                lurkcycle+=1
            
    pygame.quit()
    quit()
  
 
gameLoop()

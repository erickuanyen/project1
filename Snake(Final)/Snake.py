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

# 蛇
snake_block = 16

# 字體
def font(size, Type = "SIMYOU.TTF"):
    return pygame.font.SysFont(Type, size)

# 宣布
def message(msg, font, color, pos):
    mesg = font.render(msg, True, color)
    dis.blit(mesg, pos)

# 畫蛇(1P)
def draw_snake(snake_body, snake_block):
    for i in snake_body:
        pygame.draw.rect(dis, blue, [i[0], i[1], snake_block, snake_block])
        
# 畫蛇(2P)
def draw_snake1(snake_body, snake_block):
    for i in snake_body:
        pygame.draw.rect(dis, indigo, [i[0], i[1], snake_block, snake_block])
def draw_snake2(snake_body, snake_block):
    for i in snake_body:
        pygame.draw.rect(dis, white, [i[0], i[1], snake_block, snake_block])
        
# 得分
def draw_score(score):
    value = disp_font.render("Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])

# 隨機移動
def random_move(X, Y):
    opt = random.randint(0,3)
    if opt == 0:
        if X == dis_width - snake_block:
            if Y == 0 or Y == dis_height - snake_block:
                random_move(X, Y)
        else:
            X += snake_block
    elif opt == 1:
        if X == 0:
            if Y == 0 or Y == dis_height - snake_block:
                random_move(X, Y)
        else:
            X -= snake_block
    elif opt == 2:
        if Y == dis_width - snake_block:
            if X == 0 or X == dis_width - snake_block:
                random_move(X, Y)
        else:
            Y -= snake_block
    else:
        if Y == 0:
            if X == 0 or X == dis_width - snake_block:
                random_move(X, Y)
        else:
            Y += snake_block
    return (X, Y)


def Classic():
    # 遊戲速度
    snake_speed = 15
    
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
            if countdown == 0:
                game_close = True
            elif countdown >= snake_speed * time:
                countdown = snake_speed * time

            #控制遊戲速度
            clock.tick(snake_speed)

            # 輸遊戲後 SPACE則繼續 ESC則關閉遊戲
            while game_close:
                dis.fill(black)
                message(f"GAME OVER!", basic_font, red, [dis_width / 2 - 120, dis_height / 2 - 15])
                message(f"Your final score is {snake_len - 3}.", basic_font, red, [dis_width / 2 - 160, dis_height / 2 + 15])

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
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_LEFT,pygame.K_UP,pygame.K_DOWN,pygame.K_RIGHT):
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
            if not (0 <= x_head <= dis_width-snake_block and 0 <= y_head <= dis_height - snake_block):
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

        menu()
        
    gameLoop()


def OnePlayerTime():
    # 遊戲速度
    snake_speed = 15

    # 計時
    def draw_timer(timer):
        value = disp_font.render("Timer: " + str(timer // snake_speed), True, green)
        dis.blit(value, [0, 20])

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
            if countdown == 0:
                game_close = True
            elif countdown >= snake_speed * time:
                countdown = snake_speed * time

            #控制遊戲速度
            clock.tick(snake_speed)

            # 輸遊戲後 SPACE則繼續 ESC則關閉遊戲
            while game_close:
                dis.fill(black)
                message(f"GAME OVER!", basic_font, red, [dis_width / 2 - 120, dis_height / 2 - 15])
                message(f"Your final score is {snake_len - 3}.", basic_font, red, [dis_width / 2 - 160, dis_height / 2 + 15])

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
            if not (0 <= x_head <= dis_width - snake_block and 0 <= y_head <= dis_height - snake_block):
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
            draw_timer(countdown)
            pygame.display.update()

            # 吃到蘋果
            for k1 in range(Qa):
                if x_head == x_apple[k1] and y_head == y_apple[k1]:
                    while [x_apple[k1], y_apple[k1]] in snake_body:
                        x_apple[k1] = int(random.randint(0, dis_width) / snake_block) * snake_block
                        y_apple[k1] = int(random.randint(0, dis_height) / snake_block) * snake_block
                    snake_len += 1

            # 吃到香蕉
            for k2 in range(Qb):
                if x_head == x_banana[k2] and y_head == y_banana[k2]:
                    while [x_banana[k2], y_banana[k2]] in snake_body:
                        x_banana[k2] = int(random.randint(0, dis_width) / snake_block) * snake_block
                        y_banana[k2] = int(random.randint(0, dis_height) / snake_block) * snake_block
                    snake_len += 5

            # 吃到橘子
            for k3 in range(Qo):
                if x_head == x_orange[k3] and y_head == y_orange[k3]:
                    while [x_orange[k3], y_orange[k3]] in snake_body:
                        x_orange[k3] = int(random.randint(0, dis_width) / snake_block) * snake_block
                        y_orange[k3] = int(random.randint(0, dis_height) / snake_block) * snake_block
                    countdown+=random.randint(1, 5) * snake_speed

            # 吃到炸彈
            for k4 in range(Qe):
                if x_head == x_bomb[k4] and y_head == y_bomb[k4]:
                    game_close = True

            # 時間循環要移動
            if game_start ==True:
                countdown -= 1
                if movecycle % (item_move * snake_speed) == 0 and movecycle != 0:
                    for j1 in range(Qa):
                        newA = random_move(x_apple[j1],y_apple[j1])
                        (x_apple[j1],y_apple[j1]) = newA
                    for j2 in range(Qo):
                        newO = random_move(x_orange[j2],y_orange[j2])
                        (x_orange[j2],y_orange[j2]) = newO
                    movecycle = 0
                else:
                    movecycle += 1
                if bananacycle % (banana_lurk * snake_speed) == 0 and bananacycle != 0:
                    for l1 in range(Qb):
                        x_banana[l1] = int(random.randint(0, dis_width) / snake_block) * snake_block
                        y_banana[l1] = int(random.randint(0, dis_height) / snake_block) * snake_block
                        bananacycle = 0
                else:
                    bananacycle += 1

                if lurkcycle % (bomb_lurk * snake_speed) == 0 and lurkcycle != 0:
                    for m1 in range(Qe):
                        x_bomb[m1] = int(random.randint(0, dis_width) / snake_block) * snake_block
                        y_bomb[m1] = int(random.randint(0, dis_height) / snake_block) * snake_block
                        lurkcycle = 0
                else:
                    lurkcycle += 1

        menu()

    gameLoop()

    
def TwoPlayerTime():
    # 遊戲速度
    snake_speed = 10

    # 計時
    def draw_timer1(timer):
        value = disp_font.render("Timer01: " + str(timer//snake_speed), True, green)
        dis.blit(value, [0, 0])
    def draw_timer2(timer):
        value = disp_font.render("Timer02: " + str(timer//snake_speed), True, green)
        dis.blit(value, [0, 20])

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
        countdown1 = snake_speed * time
        countdown2 = snake_speed * time
        movecycle, lurkcycle, bananacycle = 0, 0, 0
        item_move = 5
        bomb_lurk = 5
        banana_lurk = 1
        p1timeup, p2timeup = 0, 0
        p1bombtouch, p2bombtouch = 0, 0
        p1walltouch, p2walltouch = 0, 0
        p1selftouch, p2selftouch = 0, 0
        
        # 遊戲中
        while not game_over:
            if countdown1 == 0:
                game_close = True
                p1timeup = 1
            elif countdown2 == 0:
                game_close = True
                p2timeup = 1
            elif countdown1 >= snake_speed * time:
                countdown1 = snake_speed * time
            elif countdown2 >= snake_speed * time:
                countdown2 = snake_speed * time

            #控制遊戲速度
            clock.tick(snake_speed)

            # 輸遊戲後 SPACE則繼續 ESC則關閉遊戲
            while game_close == True:
                dis.fill(black)
                if p1timeup == 1 or p1bombtouch == 1 or p1walltouch==1 or p1selftouch==1:
                    message("GAME OVER. Player 2 wins!", basic_font, red, [dis_width / 2 - 210, dis_height / 2])
                elif p2timeup==1 or p2bombtouch == 1 or p2walltouch==1 or p2selftouch==1:
                    message("GAME OVER. Player 1 win!", basic_font, red, [dis_width / 2 - 210, dis_height / 2])

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
            if not (0 <= x1_head <= dis_width - snake_block and 0 <= y1_head <= dis_height - snake_block):
                p1walltouch = 1
                game_close = True
            if not (0 <= x2_head <= dis_width - snake_block and 0 <= y2_head <= dis_height - snake_block):
                p2walltouch = 1
                game_close = True

            # 背景 & 道具
            dis.blit(backgroungImg, (0, 0))
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
                    countdown1 += random.randint(1, 5) * snake_speed
                if x2_head == x_orange[k3] and y2_head == y_orange[k3]:
                    while [x_orange[k3], y_orange[k3]] in snake2_body:
                        x_orange[k3] = int(random.randint(0, dis_width) / snake_block) * snake_block
                        y_orange[k3] = int(random.randint(0, dis_height) / snake_block) * snake_block
                    countdown2 += random.randint(1, 5) * snake_speed

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
                countdown1 -= 1
                countdown2 -= 1
                if movecycle % (item_move * snake_speed) == 0 and movecycle != 0:
                    for j1 in range(Qa):
                        newA = random_move(x_apple[j1],y_apple[j1])
                        (x_apple[j1],y_apple[j1]) = newA
                    for j2 in range(Qo):
                        newO = random_move(x_orange[j2],y_orange[j2])
                        (x_orange[j2],y_orange[j2]) = newO
                    movecycle = 0
                else:
                    movecycle += 1
                if bananacycle % (banana_lurk * snake_speed) == 0 and bananacycle != 0:
                    for l1 in range(Qb):
                        x_banana[l1] = int(random.randint(0, dis_width) / snake_block) * snake_block
                        y_banana[l1] = int(random.randint(0, dis_height) / snake_block) * snake_block
                        bananacycle = 0
                else:
                    bananacycle += 1

                if lurkcycle % (bomb_lurk * snake_speed) == 0 and lurkcycle != 0:
                    for m1 in range(Qe):
                        x_bomb[m1] = int(random.randint(0, dis_width) / snake_block) * snake_block
                        y_bomb[m1] = int(random.randint(0, dis_height) / snake_block) * snake_block
                        lurkcycle = 0
                else:
                    lurkcycle += 1

        menu()

    gameLoop()
    
    
def AImode():
    # 蛇（玩家＆電腦）
    snake_speed = 12
    draw_player = draw_snake1
    draw_AI = draw_snake2
    
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
                    message("GAME OVER. The AI wins!", basic_font, red, [dis_width / 2 - 190, dis_height / 2])
                elif AI_bombtouch == 1 or AI_walltouch == 1 or AI_selftouch == 1:
                    message("GAME OVER. You win!", basic_font, red, [dis_width / 2 - 170, dis_height / 2])

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
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_LEFT,pygame.K_RIGHT,pygame.K_UP,pygame.K_DOWN):
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
            if not (0 <= x1_head <= dis_width - snake_block and 0 <= y1_head <= dis_height - snake_block):
                player_walltouch = 1
                game_close = True
            if not (0 <= x2_head <= dis_width - snake_block and 0 <= y2_head <= dis_height - snake_block):
                AI_walltouch = 1
                game_close = True

             # AI遇 bump & wall & 身體時 (98%機率轉向)
            for i in range(Qe):
                if (x2_head + x2_change == x_bomb[i] and y2_head + y2_change == y_bomb[i]) and random.random() <= 0.98:
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
            if not (0 <= x2_head + x2_change <= dis_width and 0 <= y2_head + y2_change <= dis_width) and random.random() <= 0.98:
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

            # 劃出 蛇 & 分數
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

        menu()

    gameLoop()
    
    
def NoBound():
    # 遊戲速度
    snake_speed = 10

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
            snake_body.append([320- 3 * snake_block + i * snake_block, dis_height / 2])
        x_change = 0
        y_change = 0

        #牆起始
        walls = []
        for x in range(int(dis_width / snake_block)):
            if x != 19 and x != 20 and x != 21:
                for i in range(2):
                    y = random.randint(0, dis_height / snake_block)
                    walls.append([x * snake_block, y * snake_block])

        # 蘋果起始
        apple = pygame.image.load('./apple.png')
        x_apple = int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block
        y_apple = int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block

        #香蕉起始
        banana = pygame.image.load('./banana.png')
        x_banana = int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block
        y_banana = int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block

        #橘子起始
        orange = pygame.image.load('./orange.png')
        x_orange = int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block
        y_orange = int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block

        #炸彈起始
        bomb = pygame.image.load('./bomb.png')
        x_bomb = int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block
        y_bomb = int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block


        # 遊戲中
        while not game_over:

            #控制遊戲速度
            clock.tick(snake_speed)

            # 輸遊戲後 SPACE則繼續 ESC則關閉遊戲
            while game_close == True:
                dis.fill(black)
                message("GAME OVER!", basic_font, red, [dis_width / 2 - 120, dis_height / 2 - 15])
                message(f"Your final score is {snake_len - 3}.", basic_font, red, [dis_width / 2 - 160, dis_height / 2 + 15])
                
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
                    banana_count += 1
                    orange_count += 1
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
            for i in range(len(walls)):
                if x_head == walls[i][0] and y_head == walls[i][1]:
                    game_close = True

            # 背景 & 果實
            dis.blit(background, (0,0))
            dis.blit(apple, (x_apple, y_apple))
            dis.blit(bomb, (x_bomb, y_bomb))
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

            # 畫出 蛇 & 分數 
            draw_snake(snake_body, snake_block)
            draw_score(score)

            pygame.display.update()

            # 吃到蘋果
            if x_head == x_apple and y_head == y_apple:
                while [x_apple, y_apple] in snake_body or [x_apple, y_apple] in walls:
                    x_apple = int(random.randint(0, dis_width) / snake_block) * snake_block
                    y_apple = int(random.randint(0, dis_height) / snake_block) * snake_block
                snake_len += 1
                score += 1

            #吃到橘子
            if x_head == x_orange and y_head == y_orange:
                while [x_orange, y_orange] in snake_body or [x_orange, y_orange] in walls:
                    x_orange = int(random.randint(0, dis_width) / snake_block) * snake_block
                    y_orange = int(random.randint(0, dis_height) / snake_block) * snake_block
                snake_len += 1
                score += 3

            # 吃到炸彈
            if x_head == x_bomb and y_head == y_bomb:
                game_close = True

            # 吃到香蕉
            if x_head == x_banana and y_head == y_banana:
                while [x_banana, y_banana] in snake_body or [x_banana, y_banana] in walls:
                    x_banana = int(random.randint(0, dis_width) / snake_block) * snake_block
                    y_banana = int(random.randint(0, dis_height) / snake_block) * snake_block
                snake_len += 3

            #更新果實位置
            if  bomb_count % (5) == 0:
                x_bomb = int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block
                y_bomb = int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block
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

            #移動畫面:
            if x_head > 320 + 1*(snake_block):
                walls = walls[2 : ]
                new_r_walls = []
                for i in range(len(walls)):
                    walls[i][0] -= 1* snake_block  
                for i in range(2):
                    new_r_walls.append([dis_width,random.randint(0, dis_height/snake_block)*snake_block])
                walls = walls + new_r_walls
                x_orange -= 1 * snake_block
                x_apple -= 1 * snake_block
                x_banana -= 1 * snake_block
                x_bomb -= 1 * snake_block
                for i in range(len(snake_body)):
                    snake_body[i][0] -= 1 * snake_block

            if x_head < 320 - 1*(snake_block):
                walls = walls[ : -2]
                new_l_walls = []
                for i in range(len(walls)):
                    walls[i][0] += 1*snake_block
                for i in range(2):
                    new_l_walls.append([0,random.randint(0, dis_height/snake_block)*snake_block])
                walls = new_l_walls + walls
                x_orange += 1 * snake_block
                x_apple += 1 * snake_block
                x_banana += 1 * snake_block
                x_bomb += 1 * snake_block
                for i in range(len(snake_body)):
                    snake_body[i][0] += 1 * snake_block

            if x_apple < 0 or x_apple > dis_width:
                x_apple = int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block
                y_apple = int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block
                while [x_apple, y_apple] in walls:
                    x_apple = int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block
                    y_apple = int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block
            if x_orange < 0 or x_orange > dis_width:
                x_orange = int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block
                y_orange = int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block
                while [x_orange, y_orange] in walls:
                    x_orange = int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block
                    y_orange = int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block
            if x_bomb < 0 or x_bomb > dis_width:
                x_bomb = int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block
                y_bomb = int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block
                while [x_bomb, y_bomb] in walls:
                    x_bomb = int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block
                    y_bomb = int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block
            if x_banana < 0 or x_banana > dis_width:
                x_banana = int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block
                y_banana = int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block
                while [x_banana, y_banana] in walls:
                    x_banana = int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block
                    y_banana = int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block

        menu()

    gameLoop()
    
    
def TurnLimit():
    # 遊戲速度
    snake_speed = 10

    #轉向
    def draw_turns(turn):
        value = basic_font.render(f'Left Turns: {turn}', True, blue)
        dis.blit(value, [0, 20])

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
        mod_width = dis_width / snake_block
        mod_height = dis_height / snake_block

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
            walls.append([random.randint(0, mod_width) * snake_block, random.randint(0, mod_height) * snake_block])

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
                message("GAME OVER!", basic_font, red, [dis_width / 2 - 120, dis_height / 2 - 15])
                message(f"Your final score is {snake_len - 3}.", basic_font, red, [dis_width / 2 - 160, dis_height / 2 + 15])

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

        menu()

    gameLoop()
    

def OnePlayerPacMan():
    dis = pygame.display.set_mode((dis_width, dis_height))
    snake_speed = 15

    # 主程式
    def gameLoop():
        game_over = False
        game_close = False
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
        appleImg = pygame.image.load('apple.png')
        x_apple = int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block
        y_apple = int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block

        # 鬼起始
        ghostImg = pygame.image.load("pac.png")
        x_ghost = int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block
        y_ghost = int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block

        # 遊戲中
        while not game_over:
            #控制遊戲速度
            clock.tick(snake_speed)

            # 輸遊戲後 SPACE則繼續 ESC則關閉遊戲
            while game_close == True:
                dis.fill(black)
                message("GAME OVER!", basic_font, red, [dis_width / 2 - 120, dis_height / 2 - 15])
                message(f"Your final score is {snake_len - 3}.", basic_font, red, [dis_width / 2 - 160, dis_height / 2 + 15])

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
            if not (0 <= x_head <= dis_width - snake_block and 0 <= y_head <= dis_height - snake_block):
                game_close = True

            # 背景 & 蘋果 & 鬼
            dis.blit(backgroungImg, (0,0))
            dis.blit(appleImg, (x_apple, y_apple))
            dis.blit(ghostImg, (x_ghost, y_ghost))

            #鬼的移動
            info = pygame.display.Info() 
            sw = info.current_w 
            sh = info.current_h
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                dx = int((x_head - x_ghost) / 6)
                dy = int((y_head - y_ghost) / 6)
                x_ghost += dx
                y_ghost += dy
                for i in range(len(snake_body)-1):
                    if ((snake_body[i][0] - x_ghost)* (x_ghost - snake_body[i+1][0]))>= -256 and ((snake_body[i][1] - y_ghost)* (y_ghost - snake_body[i+1][1]))>= -256:
                        game_close = True
                if x_ghost - dx < 0 or x_ghost + dx > sw: 
                    x_ghost = int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block
                if y_ghost - dy < 0 or y_ghost + dy > sh: 
                    y_ghost = int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block
            for i in range(len(snake_body)-1):
                if ((snake_body[i][0] - x_ghost)* (x_ghost - snake_body[i+1][0]))>= -4096 and ((snake_body[i][1] - y_ghost)* (y_ghost - snake_body[i+1][1]))>= -4096:
                    game_close = True

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
            # 被鬼抓到
            for i in range(len(snake_body)-1):
                if (x_ghost >= snake_body[i][0] and x_ghost <= snake_body[i+1][0]) and (y_ghost >= snake_body[i][1] and y_ghost <= snake_body[i+1][1]):
                    game_close = True

        menu()

    gameLoop()

    
def TwoPlayerPacMan():
    dis = pygame.display.set_mode((dis_width, dis_height))
    
    # 遊戲速度
    snake_speed = 10

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

        #鬼起始
        Qg = 1
        ghostImg = pygame.image.load("pac.png")
        x_ghost = int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block
        y_ghost = int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block

        # 蘋果起始
        Qa = 5
        x_apple = [int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block for _ in range(Qa)]
        y_apple = [int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block for _ in range(Qa)]
        appleImg = pygame.image.load('apple.png')

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
        p1timeup, p2timeup = 0, 0
        p1bombtouch, p2bombtouch = 0, 0
        p1walltouch, p2walltouch = 0, 0
        p1selftouch, p2selftouch= 0, 0
        
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
                if p1bombtouch == 1 or p1walltouch == 1 or p1selftouch == 1:
                    message("GAME OVER. Player 2 wins!", basic_font, red, [dis_width / 2 - 210, dis_height / 2])
                elif p2bombtouch == 1 or p2walltouch == 1 or p2selftouch == 1:
                    message("GAME OVER. Player 1 win!", basic_font, red, [dis_width / 2 - 210, dis_height / 2])

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
            if not (0 <= x1_head <= dis_width - snake_block and 0 <= y1_head <= dis_height - snake_block):
                p1walltouch = 1
                game_close = True
            if not (0 <= x2_head <= dis_width - snake_block and 0 <= y2_head <= dis_height - snake_block):
                p2walltouch = 1
                game_close = True

            # 背景 & 道具
            dis.blit(backgroungImg, (0,0))
            for i1 in range(Qa):
                dis.blit(appleImg, (x_apple[i1], y_apple[i1]))
            for i2 in range(Qe):
                dis.blit(bombImg, (x_bomb[i2], y_bomb[i2]))

            dis.blit(ghostImg, (x_ghost, y_ghost))

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

            # 劃出 蛇 & 分數
            draw_snake1(snake1_body, snake_block)
            draw_snake2(snake2_body, snake_block)
            pygame.display.update()
            
            #鬼的移動
            info = pygame.display.Info() 
            sw = info.current_w 
            sh = info.current_h
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN):
                if snake1_len > snake2_len :
                    x_head = x1_head
                    y_head = y1_head
                else :
                    x_head = x2_head
                    y_head = y2_head
                dx = int((x_head - x_ghost)/6)
                dy = int((y_head - y_ghost)/6)
                x_ghost +=   dx
                y_ghost +=   dy
                if x_ghost - dx < 0 or x_ghost + dx > sw: 
                    x_ghost = int(random.randint(0, dis_width - snake_block) / snake_block) * snake_block
                if y_ghost - dy < 0 or y_ghost + dy > sh: 
                    y_ghost = int(random.randint(0, dis_height - snake_block) / snake_block) * snake_block

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

            # 吃到炸彈
            for k4 in range(Qe):
                if x1_head == x_bomb[k4] and y1_head == y_bomb[k4]:
                    p1bombtouch = 1
                    game_close = True
                if x2_head == x_bomb[k4] and y2_head == y_bomb[k4]:
                    p2bombtouch = 1
                    game_close = True

            # 被鬼抓到
            paccatch1 = 0
            paccatch2 = 0
            for i in range(len(snake1_body)-1):
                if ((snake1_body[i][0] - x_ghost)* (x_ghost - snake1_body[i+1][0]))>= -4096 and ((snake1_body[i][1] - y_ghost)* (y_ghost - snake1_body[i+1][1]))>= -4096:
                    paccatch1 = 1
                    game_close = True

            for i in range(len(snake2_body)-1):
                if ((snake2_body[i][0] - x_ghost)* (x_ghost - snake2_body[i+1][0]))>= -4096 and ((snake2_body[i][1] - y_ghost)* (y_ghost - snake2_body[i+1][1]))>= -4096:
                    paccatch2 = 1
                    game_close = True

        menu()

    gameLoop()
    
    
Font0 = pygame.font.SysFont('algerian', 50)
Font1 = pygame.font.SysFont('gabriola', 25)
Font2 = pygame.font.SysFont('inkfree', 40)
Font3 = pygame.font.SysFont('mvbodi', 40)
Font4 = pygame.font.SysFont('segoescript', 25)
Font5 = pygame.font.SysFont('bauhaus93', 40)
Font6 = pygame.font.SysFont('bodoniblack', 30)
Font7 = pygame.font.SysFont('bradleyhandict', 40)
Font8 = pygame.font.SysFont('castellar', 20)
Font9 = pygame.font.SysFont('curlz', 40)

disp_font = font(40)
basic_font = Font6


def menu():
    # 標題
    def Title():
        mesg = Font0.render("THE SNAKE", True, yellow)
        dis.blit(mesg, [dis_width / 2 - 9 * 3, int(dis_height / 6)])
    
    def menu_bg():
        dis.blit(menu_background, (0, 0))
        dis.blit(menu_snake, (0, 0))

    # 選項
    def choose(msg, pos):
        mesg = Font9.render(msg, True, white)
        dis.blit(mesg, pos)
    
    # 選項（被選中）
    def chosen(msg, pos):
        mesg = Font2.render(msg, True, white)
        dis.blit(mesg, pos)
        
    def CREDIT(msg, pos):
        mesg = Font4.render(msg, True, white)
        dis.blit(mesg, pos)

    def HELP(msg, pos):
        mesg = Font1.render(msg, True, white)
        dis.blit(mesg, pos)

    menu_snake = pygame.image.load('./menu_snake.png')
    menu_background = pygame.Surface(dis.get_size())
    menu_background = menu_background.convert()
    menu_background.fill(black) 
    game_selected = False

    menu_bg()
    Title()
    info_menu = [
        ["1-Player", [dis_width / 1.75 + 8, dis_height / 3], 1],
        ["2-Player", [dis_width / 1.75 + 8, dis_height / 3 + 50], 0],
        ["Help", [dis_width / 1.75 + 30, dis_height / 3 + 100], 0],
        ["Credits", [dis_width / 1.75 + 16, dis_height / 3 + 150], 0]
    ]
    info_1P = [
        ["Classic", [dis_width / 1.75 + 8, dis_height / 3], 1],
        ["Time Limit", [dis_width / 1.75 + 8, dis_height / 3 + 50], 0],
        ["No Bound", [dis_width / 1.75 + 8, dis_height / 3 + 100], 0],
        ["AI", [dis_width / 1.75 + 40, dis_height / 3 + 150], 0],
        ["Turn Limit", [dis_width / 1.75 + 8, dis_height / 3 + 200], 0],
        ["Pac Man", [dis_width / 1.75 + 8, dis_height / 3 + 250], 0]
    ]
    info_2P = [
        ["Time Limit", [dis_width / 1.75 + 8, dis_height / 3], 1],
        ["Pac Man", [dis_width / 1.75 + 8, dis_height / 3 + 50], 0]
    ]
    info_credit = [
        ["B09901076", [dis_width / 2, dis_height / 3], 3], 
        ["GUAN-YAN LIN", [dis_width / 2, dis_height / 3 + 30], 3],
        ["B09901141", [dis_width / 2, dis_height / 3 + 80], 3],
        ["SHENG-DING WU", [dis_width / 2, dis_height / 3 + 110], 3],
        ["B09901147", [dis_width / 2, dis_height / 3 + 160], 3],
        ["BAO-REI LIN", [dis_width / 2, dis_height / 3 + 190], 3],
        ["B09901151", [dis_width / 2, dis_height / 3 + 240], 3],
        ["MING-CHI CHIOU", [dis_width / 2, dis_height / 3 + 270], 3]
    ]
    info_help = [
        ["--ESC--", [50, 50], 2],
        ["In Games: Back to Menu", [100, 75], 2],
        ["In Menu: Close the game", [100, 100], 2],
        ["--Space--", [50, 140], 2],
        ["When the game is over, press to play again", [100, 165], 2],
        ["--Enter & Right--", [50, 205], 2],
        ["Select on Menu", [100, 230], 2],
        ["--Left--", [50, 270], 2],
        ["Back to Menu", [100, 295], 2],
        ["--In Games--", [50, 335], 2],
        ["1-Player & 1P player: Use Up, Down,  Left, Right", [100, 360], 2],
        ["2P player: Use W, A, S, D", [100, 385], 2],
        ]
    info_help_Classic = [
        ["Classic", [20, 20], 5],
        ["--Apple--", [50, 50], 2],
        ["Score +1", [100, 75], 2],
        ["--Bomb--", [50, 115], 2],
        ["Touch them then gameover", [100, 140], 2]
    ]
    
    info = info_menu
    for i in info:
        if i[-1] == 0:
            choose(i[0], i[1])
        elif i[-1] == 1:
            chosen(i[0], i[1])
        
                
    while not game_selected:
        pygame.display.update()
        for i in info:
            if i[-1] == 0:
                choose(i[0], i[1])
            elif i[-1] == 1:
                chosen(i[0], i[1])
            elif i[-1] == 2:
                HELP(i[0], i[1])
            elif i[-1] == 3:
                CREDIT(i[0], i[1])
            elif i[-1] == 4:
                message(i[0], Font8, white, i[1])
            elif i[-1] == 5:
                message(i[0], Font7, white, i[1])

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                menu_bg()
                Title()
                if event.key == pygame.K_DOWN and info[-1][2] != 1:
                    if info in (info_menu, info_1P, info_2P):
                        next_chosen = 0
                        for i in info:
                            if i[2] == 1:
                                choose(i[0], i[1])
                                next_chosen = 1
                                i[2] = 0
                            elif next_chosen == 1:
                                chosen(i[0], i[1])
                                next_chosen = 0
                                i[2] = 1
                            else:
                                choose(i[0], i[1])
                    elif info == info_help:
                        dis.blit(menu_background, (0, 0))
                elif event.key == pygame.K_UP and info[0][2] != 1:
                    if info in (info_menu, info_1P, info_2P):
                        next_chosen = 0
                        for i in info[::-1]:
                            if i[2] == 1:
                                choose(i[0], i[1])
                                next_chosen = 1
                                i[2] = 0
                            elif next_chosen == 1:
                                chosen(i[0], i[1])
                                next_chosen = 0
                                i[2] = 1
                            else:
                                choose(i[0], i[1])
                    elif info == info_help:
                        dis.blit(menu_background, (0, 0))
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_RIGHT):
                    if info in (info_menu, info_1P, info_2P):
                        k = 0
                        for i in range(len(info)):
                            if info[i][2] == 1:
                                k = i
                                break
                    if k == 0:
                        if info == info_menu:
                            info = info_1P
                        elif info == info_1P:
                            Classic()
                            game_selected = True
                        else:
                            TwoPlayerTime()
                            game_selected = True
                    elif k == 1:
                        if info == info_menu:
                            info = info_2P
                        elif info == info_1P:
                            OnePlayerTime()
                            game_selected = True
                        else:
                            TwoPlayerPacMan()
                            game_selected = True
                    elif k == 2:
                        if info in (info_menu, info_help):
                            dis.blit(menu_background, (0, 0))
                            info = info_help
                        else:
                            NoBound()
                            game_selected = True
                    elif k == 3:
                        if info in (info_menu, info_credit):
                            info = info_credit
                        else:
                            AImode()
                            game_selected = True
                    elif k == 4:
                        TurnLimit()
                        game_selected = True
                    elif k == 5:
                        OnePlayerPacMan()
                        game_selected = True
                elif event.key == pygame.K_LEFT:
                    info = info_menu
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
        
menu()

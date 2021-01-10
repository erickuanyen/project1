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
snake_speed = 12
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
    background = pygame.image.load('./grid.png')
    score = 0
    bomb_count = 1
    banana_count = 1
    orange_count = 1
    
    # 蛇起始
    snake_len = 3
    snake_body = []
    for i in range(snake_len):
        snake_body.append([320- 3*snake_block + i * snake_block, dis_height / 2])
    x_change = 0
    y_change = 0

    #牆起始
    walls = []
    for x in range(int(dis_width/snake_block)):
        if x != 19 and x != 20 and x != 21:
            for i in range(2):
                y = random.randint(0,dis_height/snake_block)
                walls.append([x*snake_block, y*snake_block])

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
            message(f"You Lost! You got {score} scores! Press 'space'--play again or 'esc'--quit", red)
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
    
            
            
            

            
            
            
            
    pygame.quit()
    quit()
  
 
gameLoop()

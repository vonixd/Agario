import pygame
import math
import random
pygame.init()
w_width = 1600
w_height = 900
bg = (220, 220, 200)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
purple = (255,0,255)
colors = [white, red, green, blue, purple]
win = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption("agario")
clock = pygame.time.Clock()
main_font = pygame.font.SysFont('comicsans', 30)



class Circle(object):
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = colors[2]
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)


class Food(object):
    def __init__(self, x, y, radius, speed = 0, dx = 0, dy = 0):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = random.choice(colors)
        self.speed = speed
        self.dx = dx
        self.dy = dy

    def draw(self, win):


        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

    def get_pos(self):
        return self.x, self.y
    def moving(self):
        if self.speed > 0:
            distance = (self.dx**2 + self.dy**2)**0.5
            self.x += (self.dx/distance) * self.speed
            self.y += (self.dy/distance) * self.speed
            self.speed -= 0.4

            self.x = max(0, min(w_width, self.x))
            self.y = max(0, min(w_height, self.y))






class Enemy(Circle):
    def __init__(self, x, y,):
        self.score = 60
        self.x = x
        self.y = y
        self.radius = self.score ** 0.7
        self.color = colors[1]
        self.speed = 20 / (self.score / 4) + 1

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
    def get_pos(self):
        return self.x, self.y
    def movement(self):
        del_x = player.x - self.x
        del_y = player.y - self.y
        distance = (del_x**2 + del_y**2)**0.5
        if distance != 0:
            if distance <= 300:
                if player_score < self.score:
                    self.x += (del_x/distance) * self.speed
                    self.y += (del_y/distance) * self.speed
                if player_score >= self.score:

                    self.x -= (del_x / distance) * self.speed
                    self.y -= (del_y / distance) * self.speed

                self.x = max(0, min(w_width, self.x))
                self.y = max(0, min(w_height, self.y))
            else:
                nearest_dis = 10000
                all_list = food_list + playerw_list
                for food in all_list:
                    del_x = food.x - self.x
                    del_y = food.y - self.y
                    distance = (del_x ** 2 + del_y ** 2) ** 0.5
                    if nearest_dis > distance:
                        nearest = food
                        nearest_dis = distance
                del_x = nearest.x - self.x
                del_y = nearest.y - self.y
                distance = (del_x ** 2 + del_y ** 2) ** 0.5
                self.x += (del_x/distance)*self.speed
                self.y += (del_y/distance)*self.speed














def player_movement():
    pos_x, pos_y = pygame.mouse.get_pos()
    del_x = pos_x-player.x
    del_y = pos_y-player.y
    distance = ((del_x**2) + (del_y**2))**0.5
    if distance != 0:
        player.x += (del_x/distance) * player_speed
        player.y += (del_y/distance) * player_speed





def writing(tekst, x, y, color = (0,0,0)):
    text = main_font.render(tekst, True, color)
    win.blit(text, (x, y))

def collision(x1, y1, r1, x2, y2, r2):
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance < max(r1,r2)




def redrawWindow():
    i = 1
    win.fill(bg)
    for enemy in enemy_list:
        enemy.draw(win)
        writing(f'Enemy {i}', enemy.x-(enemy.radius/2) , enemy.y-(enemy.radius/2))
        writing(f'{enemy.score}', enemy.x-(enemy.radius/2) , enemy.y-(enemy.radius/2)+20)
        i += 1
    for food in food_list:
        food.draw(win)
    for food in playerw_list:
        food.draw(win)
    player.draw(win)
    writing(f'score: {player_score}', w_width-len((f'score: {player_score}')*10)-50,20 )
    writing("Player" , player.x-(player.radius/2) , player.y)
    pygame.display.update()




food_list = []
enemy_list = []
playerw_list = []
player_score = 40
player = Circle(400, 400, player_score ** 0.7)
player_speed = 20 / (player_score / 4) + 1

run = True
# generate food

while run:
    clock.tick(100)
    pos_x, pos_y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    player_movement()
    for food in playerw_list:
        food.moving()
    # generate food
    if len(food_list) < 200:
        food_list.append(Food(random.randrange(50, 1550), random.randrange(50, 850), 10))

    # eat food
    all_list = food_list + playerw_list
    for food in all_list:
        if collision(food.x,food.y,food.radius,player.x,player.y,player.radius):
            if food in food_list:
                food_list.remove(food)
            else:
                playerw_list.remove(food)
            player_score += 1
            player.radius = player_score ** 0.7
            player_speed = 20 / (player_score / 4) + 1
    #respawn enemy
    if len(enemy_list) < 3:
        enemy_list.append(Enemy(random.randrange(50,1550), random.randrange(50, 850)))

    #collision enemy
    for enemy in enemy_list:
        enemy.movement()
        if collision(player.x,player.y,player.radius,enemy.x,enemy.y,enemy.radius):
            if player_score > enemy.score:
                enemy_list.remove(enemy)
                player_score += enemy.score
                player.radius = player_score ** 0.7
                player_speed = 20 / (player_score / 4) +1
            if player_score < enemy.score:
                run = False
        #enemy eat food
        for enemy in enemy_list:
            all_list = food_list + playerw_list
            for food in all_list:
                if collision(food.x,food.y,food.radius,enemy.x,enemy.y,enemy.radius):
                    if food in food_list:
                        food_list.remove(food)
                    else:
                        playerw_list.remove(food)
                    enemy.score += 1
                    enemy.radius = enemy.score ** 0.7
                    enemy.speed = 20 / (enemy.score / 4) + 1






    keys = pygame.key.get_pressed()


    if keys[pygame.K_w]:
        if player_score >= 20:
            del_x = pos_x - player.x
            del_y = pos_y - player.y
            distance = ((del_x ** 2) + (del_y ** 2)) ** 0.5
            playerw_list.append(Food(player.x + (del_x/distance)*player.radius*1.2 , player.y + (del_y/distance)*player.radius*1.2, 10, 12, del_x, del_y))
            player_score -= 1
            player.radius = player_score ** 0.7
            player_speed = 20 / (player_score / 4) + 1
    if keys[pygame.K_SPACE] and player_score >=20:
        player_speed = 20
        player_score -= round(player_score/100)

    redrawWindow()

pygame.quit()


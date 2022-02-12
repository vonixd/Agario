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
    def __init__(self, x, y, radius, speed = 0):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = random.choice(colors)
        self.speed = speed
    def draw(self, win):


        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

    def get_pos(self):
        return self.x, self.y



class Enemy(Circle):
    def __init__(self, x, y, radius,):
        self.score = 60
        self.x = x
        self.y = y
        self.radius = radius
        self.color = colors[1]
        self.speed = 1

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
    def get_pos(self):
        return self.x, self.y
    def movement(self):

        if player_score < self.score:
            if player.y > self.y and self.y >= 0 and self.y < w_height:
                self.y += self.speed
            if player.y < self.y and self.y >= 0 and self.y < w_height:
                self.y -= self.speed
            if player.x > self.x and self.x >= 0 and self.x < w_width:
                self.x += self.speed
            if player.x < self.x and self.x >= 0 and self.x < w_width:
                self.x -= self.speed
        if player_score > self.score:
            if player.x - self.x >= player.radius  or player.y - self.y >= player.radius:
                self.x = self.x
                self.y = self.y
            elif player.x - self.x <= 10  or player.y - self.y <=10 :
                if player.y > self.y and self.y >= 0 and self.y < w_height:
                    self.y -= self.speed
                if player.y < self.y  and self.y >= 0 and self.y < w_height:
                    self.y += self.speed
                if player.x > self.x and self.x >= 0 and self.x < w_width:
                    self.x -= self.speed
                if player.x < self.x and self.x >= 0 and self.x < w_width:
                    self.x += self.speed





def player_movement():
    pos_x, pos_y = pygame.mouse.get_pos()
    if player.y > pos_y :
        player.y -= player_speed
    if player.y < pos_y:
        player.y += player_speed
    if player.x > pos_x:
        player.x -= player_speed
    if player.x < pos_x:
        player.x += player_speed




def writing(tekst, x, y, color = (0,0,0)):
    text = main_font.render(tekst, 1, color)
    win.blit(text, (x, y))



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
    player.draw(win)
    writing(f'score: {player_score}', w_width-len((f'score: {player_score}')*10)-50,20 )
    writing("Player" , player.x-(player.radius/2) , player.y)
    pygame.display.update()




food_list = []
enemy_list = []
player_score = 40
player = Circle(400, 400, 5)
player_speed = 10

run = True
# generate food

while run:
    clock.tick(100)
    pos_x, pos_y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    player_movement()
    # generate food
    if len(food_list) < 200:
        food_list.append(Food(random.randrange(50, 1550), random.randrange(50, 850), 10))

    # eat food
    for food in food_list:
        if food.x <= player.x + player.radius and food.x >= player.x - player.radius:
            if food.y <= player.y + player.radius and food.y >= player.y - player.radius:
                food_list.remove(food)
                player_score += 1
                player.radius = player_score / 4
                player_speed = 20 / (player_score / 4)
    #respawn enemy
    if len(enemy_list) < 3:
        enemy_list.append(Enemy(random.randrange(50,1550), random.randrange(50, 850), 10))

    #collision enemy
    for enemy in enemy_list:
        enemy.movement()
        if enemy.x <= player.x + player.radius and enemy.x >= player.x - player.radius:
            if enemy.y <= player.y + player.radius and enemy.y >= player.y - player.radius:
                if player_score > enemy.score:
                    enemy_list.remove(enemy)
                    player_score += enemy.score
                    player.radius = player_score / 4
                    player_speed = 20 / (player_score / 4)
                if player_score < enemy.score:
                    run = False
        #enemy eat food
        for enemy in enemy_list:
            for food in food_list:
                if food.x <= enemy.x + enemy.radius and food.x >= enemy.x - enemy.radius:
                    if food.y <= enemy.y + enemy.radius and food.y >= enemy.y - enemy.radius:
                        food_list.remove(food)
                        enemy.score += 1
                        enemy.radius = enemy.score / 4
                        enemy.speed = 20 / (enemy.score / 2)






    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        if player_score >= 20:
            food_list.append(Food(pos_x, pos_y, 10))
            player_score -= 1
            player.radius = player_score / 4
            player_speed = 20 / (player_score / 4)
    if keys[pygame.K_t]:
        player.x = pos_x
        player.y = pos_y
    redrawWindow()

pygame.quit()


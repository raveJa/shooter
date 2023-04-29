from pygame import *
from random import randint
from time import time as timer

t = timer()

window = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
clock = time.Clock()


x1 = 450
y1 = 689




class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 2:
            self.rect.x -= 5
        if keys_pressed[K_d] and self.rect.x < 620:
            self.rect.x += 5
    def fire(self):
        global snaryd
        self.sprite_center = self.rect.centerx
        self.Sprite_top = self.rect.top
        keys_pressed = key.get_pressed()
        if keys_pressed[K_SPACE]:
            pyla.add(Bullet('bullet.png', self.rect.centerx, self.rect.top, 2))
            snaryd = snaryd -1
            

lost = 0

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = transform.scale(image.load(player_image), (100, 50))
    def update(self):
        self.rect.y +=randint(1, 2)
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(10, 680) 
            lost = lost + 1

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = transform.scale(image.load(player_image), (10, 20))
    def update(self):
        self.rect.y -= 2
        if self.rect.y < 0:
            self.kill()
 
class cometa(Enemy):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = transform.scale(image.load(player_image), (100, 50))
    def update(self):
        self.rect.y +=randint(1, 2)
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(10, 680) 


        
start = timer()







num_fire = 0
win_chek = 0  
heal = 3
snaryd = 5



font.init()
font = font.Font(None, 36)
text_lose = font.render('Пропущено:' + str(lost), 1, (255, 255, 255))   
text_win = font.render('Попал:' + str(win_chek), 1, (255, 255, 255))
win_font = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (125, 0, 0))
hp = font.render('Хп:' + str(heal), 1, (125, 125, 125))
peresar = font.render('Wait...', 1, (255, 255, 255))
ammo = font.render('Осталось:' + str(snaryd), 1, (125, 125, 125))

        




game = True
win = False


shar = sprite.Group()
shar.add(cometa('asteroid.png',190,88, 1))
shar.add(cometa('asteroid.png',390,108, 1))




p1 = Player('rocket.png',320,420,50)
pyla = sprite.Group()


monsters = sprite.Group()
monsters.add(Enemy('ufo.png',200,120, randint(1, 2)))
monsters.add(Enemy('ufo.png',490,100, randint(1, 2)))
monsters.add(Enemy('ufo.png',350,90, randint(1, 2)))
monsters.add(Enemy('ufo.png',420,50, randint(1, 2)))
monsters.add(Enemy('ufo.png',560,20, randint(1, 2)))

while game:
    text_lose = font.render('Пропущено:' + str(lost), 1, (255, 255, 255))
    text_win = font.render('Попал:' + str(win_chek), 1, (255, 255, 255))  
    hp = font.render('Хп:' + str(heal), 1, (255, 255, 255))
    peresar = font.render('Wait...', 1, (255, 255, 255))
    ammo = font.render('Осталось:' + str(snaryd), 1, (125, 125, 125))

    window.blit(hp, (0, 0))  
    window.blit(background,(0, 0))
    window.blit(text_lose, (0, 0))
    window.blit(text_win,(20, 20))
    for e in event.get():
        if e.type == QUIT:
            game = False

    sprites_list = sprite.groupcollide(monsters, pyla, True, True)
    for i in sprites_list:
        win_chek = win_chek +1
        monsters.add(Enemy('ufo.png',randint(100,650), 20, randint(1, 2)))
    if win != True:
        window.blit(background,(0, 0))
        window.blit(text_lose, (0, 0))
        window.blit(text_win,(20, 20))
        window.blit(hp, (620, 0))
        window.blit(ammo, (350, 0))
        #игрок
        p1.update()
        p1.reset()
        p1.fire()
        #враг
        monsters.update()
        monsters.draw(window) 
        #пуля
        pyla.update()
        pyla.draw(window)
        #камета
        shar.update()
        shar.draw(window)
        

    if win_chek >= 10 :
        win = True
        window.blit(win_font, (300, 250))

    if lost >= 10:
        win = True
        window.blit(lose, (300, 250))


    if sprite.spritecollide(p1, monsters, True):
        heal = heal -1
        window.blit(hp, (680, 480))

    if sprite.spritecollide(p1, shar, True):
        heal = heal -3
        window.blit(hp, (680, 480))

    if heal <= 0:
        win = True
        window.blit(lose, (300, 250))

    #if ammo <= 0:
        #peresar = True
        #del keys_pressed[K_SPACE]

    


    

        

        

    
        

    
        

        



                
            

    clock = time.Clock()
    FPS = 60
    display.update()
#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        
        
        
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))   
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 100:
            self.rect.x += self.speed
    
 
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 30, 30, -15)
        bullets.add(bullet)
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()        
#####
    
#######
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            
            self.rect.x = randint(105, win_width - 105)
            self.rect.y = 0
            
            lost = lost + 1
clock = time.Clock()
FPS = 60
speed = 6

win_height = 800
win_width = 1000
window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("galaxy.jpg"), (1000, 800))
lost = 0
score = 0
font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 36)
text_lose = font1.render('You lose', True, (255, 255, 255))
text_score = font2.render('You win',True, (255, 255, 255))
rel_time = False
now_time = 0
last_time = 0
num_fire = 0
hp = 3
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
#money = mixer.Sound('win.mp3')
fire_sound = mixer.Sound('fire.ogg')
#ship = transform.scale(image.load("rocket.png"), (100, 100))
cyborg = transform.scale(image.load("ufo.png"), (100, 100))
player = Player('rocket.png', 500, 700, 100, 100, speed)
asteroid = transform.scale(image.load("asteroid.png"), (500, 500))
#cyborg = Enemy(, 900, 200, 3)
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(105, win_width - 105), -40, 80, 50,  randint(1, 3))
    monsters.add(monster)
for i in range(1, 6):
    asteroid = Enemy('asteroid.png', randint(105, win_width - 105), -40, 80, 50,  randint(1, 3))
    asteroids.add(asteroid)


game = True
finish = False
while game:   
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()
                if num_fire < 5 and rel_time == False:
                    pass
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if finish != True:
        window.blit(background,(0, 0))
     
       
        monsters.update()
        player.update()
        bullets.update()
        player.reset()
        bullets.draw(window)
        monsters.draw(window)
        player.reset()
        asteroids.update()
        asteroids.draw(window)

        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10,50))

        text_score = font2.render('Cчет: ' + str(score), 1, (255, 255, 255))
        window.blit(text_score, (10, 80))
        
        text_hp = font2.render('Жизни: ' + str(hp), 1, (255, 255, 255))
        window.blit(text_hp, (10, 110))
       
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('ufo.png', randint(105, win_width - 105), -40, 80, 50,  randint(1, 5))
            monsters.add(monster)
            


        if score >= 50:
            finish = True
            window.blit(text_score, (10, 80))

        if sprite.spritecollide(player, monsters, False) or lost >= 8:
            finish = True   
            window.blit(text_lose, (10,50))
        if sprite.spritecollide(player, asteroids, True, False) or lost >= 8:
            if hp <= 0 :

                finish = True
                window.blit(text_hp, (10,110))  
            hp -= 1
#    keys_pressed = key.get_pressed()
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Перезарядка...', 1, (255, 255, 0))
                window.blit(reload, (500, 500))
            else:
                num_fire = 0
                rel_time = False
            





    clock.tick(FPS)
    display.update()
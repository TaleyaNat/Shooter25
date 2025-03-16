from pygame import *
from random import randint
# описание классов
class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__()
        self.image = transform.scale(image.load(img), (w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))    

    def collidepoint(self, x,y):
        return self.rect.collidepoint(x,y)



class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x>10:
            self.rect.x-=self.speed
        if keys[K_RIGHT] and self.rect.x<700 -10- self.rect.width:
            self.rect.x+=self.speed

    def fire(self):
        bullet = Bullet('bullet.png', 
        self.rect.centerx, self.rect.y,15, 30, 5)
        bullets.add(bullet)
    
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500-self.rect.height:
            self.rect.x = randint(10, 700-10-self.rect.width)
            self.rect.y = -self.rect.height
            self.speed = randint(2,5)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
            


# создай окно игры
window = display.set_mode((700,500))
display.set_caption('Шутер')
#задай фон сцены
background = transform.scale(image.load('galaxy.jpg'), (700,500))
#подключение музыки
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
#работа со шрифтами
font.init()
# font1 = font.Font(None, 36)
font1 = font.SysFont('Arial', 36)

#создаем спрайты
player = Player('rocket.png', 316,400,68, 100, 5)

bullets = sprite.Group()

enemy_count = 6
enemyes = sprite.Group()
for i in range(enemy_count):
    enemy = Enemy('ufo.png', randint(10, 700-10-70), -40, 70, 40, randint(2,5))
    enemyes.add(enemy)

button = GameSprite(
    'play_but.png', 300, 200, 
    100, 50, 0)

game = True
finish = True
menu = True
lost = 0  #счетчик пропущенных врагов
score = 0 #счетчик убитых врагов
clock = time.Clock()
fps = 60
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()

    if menu:
        window.blit(background, (0,0))
        button.reset()
        pressed = mouse.get_pressed()
        pos = mouse.get_pos()
        if pressed[0]:
            if button.collidepoint(
                pos[0], pos[1]):
                menu = False
                finish = False



    if not finish:
        window.blit(background, (0,0))

        player.update()
        player.reset()

        enemyes.update()
        enemyes.draw(window)

        bullets.update()
        bullets.draw(window)

        lost_enemy = font1.render('Пропущено: '+str(lost), 1, (255,255,255))
        window.blit(lost_enemy, (10,10))
        score_enemy = font1.render('Убито: '+str(score), 1, (255,255,255))
        window.blit(score_enemy, (10,50))

        #! проверка условий
        sprite_list = sprite.groupcollide(
            enemyes, bullets, True, True
        )
        for i in range(len(sprite_list)):
            score += 1
            enemy = Enemy(
                'ufo.png', 
                randint(10, 700-10-70), 
                -40, 70, 40, randint(2,5))
            enemyes.add(enemy)

        if score>=10:
            finish=True
            text_win = font1.render(
                'ПОБЕДА!', 1, (255,255,255))
            window.blit(text_win, (350,250))

        sprite_list = sprite.spritecollide(player, enemyes, True)
        if lost>=10 or len(sprite_list)>0:
            finish=True
            text_lose = font1.render('ПРОИГРЫШ!', 1, (255,255,255))
            window.blit(text_lose, (350,250))

    clock.tick(fps)
    display.update()

























# from pygame import *
# from random import randint
# from time import time as mytime
# #описываем классы
# class GameSprite(sprite.Sprite):
#     def __init__(self, img, x, y, w, h, speed):
#         super().__init__()
#         self.image = transform.scale(image.load(img), (w,h))
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#         self.speed = speed

#     def reset(self):
#         window.blit(self.image, (self.rect.x, self.rect.y))

#     def collidepoint(self, x, y):
#         return self.rect.collidepoint(x,y)

# class Player(GameSprite):
#     def update(self):
#         keys = key.get_pressed()
#         if keys[K_LEFT] and self.rect.x>10:
#             self.rect.x-=self.speed
#         if keys[K_RIGHT] and self.rect.x<700 -10- self.rect.width:
#             self.rect.x+=self.speed

#     def fire(self):
#         y = self.rect.y
#         x = self.rect.centerx
#         bullet = Bullet('bullet.png', x-7, y, 15,30,5)
#         bullets.add(bullet)


# class Enemy(GameSprite):
#     def update(self):
#         global lost
#         self.rect.y +=self.speed
#         if self.rect.y>500-self.rect.height:
#             self.rect.x = randint(5,700-5-self.rect.width)
#             self.rect.y = -self.rect.height
#             self.speed = randint(1,3)
#             lost +=1

# class Bullet(GameSprite):
#     def update(self):
#         self.rect.y -= self.speed
#         if self.rect.y<0:
#             self.kill()



# #создай окно игры
# window = display.set_mode((700,500))
# display.set_caption('Шутер')

# #задай фон сцены
# background = transform.scale(image.load('galaxy.jpg'), (700,500))
# button = GameSprite('button.png',300, 225, 100, 50, 0)



# #подключение музыки
# mixer.init()
# mixer.music.load('space.ogg')
# mixer.music.play()

# #подключение шрифтов
# font.init()
# font1 = font.Font(None, 36)



# #создаем спрайты
# player = Player('rocket.png', 316,400,68, 100, 5)

# enemy_count = 5
# enemyes = sprite.Group()
# for i in range(enemy_count):
#     enemy = Enemy('ufo.png', randint(5, 700-5-70),-50,70, 40, randint(1,3))
#     enemyes.add(enemy)

# asteroid_count = 3
# asteroids = sprite.Group()
# for i in range(asteroid_count):
#     asteroid = Enemy('asteroid.png', randint(5, 700-5-70),-50,70, 40, randint(1,2))
#     asteroids.add(asteroid)


# bullets = sprite.Group()

# boss = Enemy('ufo.png', randint(5, 700-5-70),-50,210, 120, randint(1,3))

# #обработай событие «клик по кнопке "Закрыть окно"»
# game = True
# finish = True
# menu = True
# lost = 0
# score = 0
# text = 0
# font_lose = font1.render('Ты проиграл!', 1, (255,255,255))
# font_win = font1.render('Ты выиграл!', 1, (255,255,255))
# boss_f = 0
# boss_l = False

# clock = time.Clock()
# FPS = 60

# while game:
#     # проверка нажатия на кнопку "выход"
#     for e in event.get():
#         if e.type == QUIT:
#             game = False
#         if e.type == KEYDOWN:
#             if e.key == K_SPACE:
#                 player.fire()
#             if e.key == K_TAB:
#                 menu = False
#                 finish = False
#                 strt_time = mytime()

#     if menu == True:
#         window.blit(background, (0,0))
#         button.reset()
#         pressed = mouse.get_pressed()
#         pos = mouse.get_pos()
#         if pressed[0]:
#             if button.collidepoint(pos[0], pos[1]):
#                 menu = False
#                 finish = False
#                 strt_time = mytime()
#         if text == 1:
#             window.blit(font_win, (250,175))
#         elif text == 2:
#             window.blit(font_lose, (250,175))
#         if text!=0:
#             font_time = font1.render('Время на уровне: '+str(int(end_time-strt_time)), 1, (255,255,255))
#             window.blit(font_time, (250,350))
#         lost = 0
#         score = 0
#         enemyes.empty()
#         for i in range(enemy_count):
#             enemy = Enemy('ufo.png', randint(5, 700-5-70),-50,70, 40, randint(1,3))
#             enemyes.add(enemy)
#         asteroids.empty()
#         for i in range(asteroid_count):
#             asteroid = Enemy('asteroid.png', randint(5, 700-5-70),-50,70, 40, randint(1,2))
#             asteroids.add(asteroid)
#         bullets.empty()
        



#     if finish!=True:
#         #рисовка объектов сцены
#         window.blit(background, (0,0))
#         player.update()
#         enemyes.update()
#         bullets.update()
#         asteroids.update()
#         player.reset()
#         enemyes.draw(window)
#         bullets.draw(window)
#         asteroids.draw(window)

#         sprite_list1 = sprite.spritecollide(player,enemyes, False)
#         sprite_list2 = sprite.spritecollide(player,asteroids, False)
#         if len(sprite_list1)>0 or len(sprite_list2)>0 or lost>3:
#             text=2
#             finish=True
#             menu=True
#             end_time = mytime()

#         sprite_list = sprite.groupcollide(enemyes, bullets, True, True)
#         for m in sprite_list:
#             score+=1
#             enemy = Enemy('ufo.png', randint(5, 700-5-70),-50,70, 40, randint(1,3))
#             enemyes.add(enemy)
#         if score>9:
#             text=1
#             finish=True
#             menu=True
#             end_time = mytime()




#         #рисовка текста
#         font_lost = font1.render('Пропущено '+str(lost), 1, (255,255,255))
#         window.blit(font_lost, (10,50))
#         font_score = font1.render('Счет '+str(score), 1, (255,255,255))
#         window.blit(font_score, (10,20))

#     # обновление окна игры
#     display.update()
#     clock.tick(FPS)





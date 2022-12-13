import pygame,random,time

from EXPLODE import *
from MUSIC import *

window_width = 630
window_height = 630


class Bullet(pygame.sprite.Sprite):
    def __init__(self,tank):
        pygame.sprite.Sprite.__init__(self)
        self.live =True
        self.image = pygame.image.load('images/bullet/missile.gif')
        self.direction = tank.direction
        self.rect = self.image.get_rect()

        if self.direction == 'U':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top - self.rect.top - 10 # 修改一下，不然子弹会与炮管重合
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2

        self.speed = 10

    def move(self):
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                self.live = False
        elif self.direction == 'D':
            if self.rect.top < 630 - self.rect.height:
                self.rect.top += self.speed
            else:
                self.live = False
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.live = False
        elif self.direction == 'R':
            if self.rect.left < 630 - self.rect.width:
                self.rect.left += self.speed
            else:
                self.live = False

    def display(self,main_game):
        main_game.window.blit(self.image,self.rect)

    def mybullet_hit_tank(self,main_game):
        for enemy in main_game.enemytank_list:
            if pygame.sprite.collide_rect(enemy,self):
                enemy.hp -= 1
                # 不把子弹消失就会一直碰撞，还是“秒杀”
                self.live = False
                hit_music = Music('audios/hit.wav')
                hit_music.play_music()
                if enemy.hp < 0:
                    enemy.live = False
                    self.live = False
                    explode = Explode(enemy)
                    main_game.explode_list.append(explode)
                    boom_music = Music('audios/bang.wav')
                    boom_music.play_music()
                    main_game.score += 100

                    main_game.enemytank_count_all -= 1
                    if main_game.enemytank_count_all >= main_game.enemytank_count_now:
                        main_game.creat_enemytank(self)

    def enemybullet_hit_mytank(self,main_game):
        if main_game.my_tank and main_game.my_tank.live:
                if pygame.sprite.collide_rect(main_game.my_tank,self):
                    explode = Explode(main_game.my_tank)
                    main_game.explode_list.append(explode)
                    self.live = False
                    boom_music = Music('audios/bang.wav')
                    boom_music.play_music()
                    main_game.my_tank.live = False
                    main_game.my_tank_life -= 1
                    main_game.ourtank_list.remove(main_game.my_tank)
                    main_game.score -=100
                    if main_game.my_tank_life < 1 and main_game.your_tank_life < 1:
                        main_game.is_gameover = True

        if main_game.your_tank and main_game.your_tank.live:
                if pygame.sprite.collide_rect(main_game.your_tank, self):
                    explode = Explode(main_game.your_tank)
                    main_game.explode_list.append(explode)
                    self.live = False
                    boom_music = Music('audios/bang.wav')
                    boom_music.play_music()
                    main_game.your_tank.live = False
                    main_game.your_tank_life -= 1
                    main_game.ourtank_list.remove(main_game.your_tank)
                    main_game.score -=100
                    if main_game.my_tank_life < 1 and main_game.your_tank_life < 1:
                        main_game.is_gameover = True

    def hit_wall(self,main_game):
        for wall in main_game.wall_list:
            if pygame.sprite.collide_rect(self,wall):
                self.live = False
                wall.hp -= 1
                if wall.hp<=0:
                    wall.live = False
                    main_game.score += 10

    def hit_home(self,main_game):
        if pygame.sprite.collide_rect(self, main_game.my_home):
            self.live = False
            main_game.my_home.alive = False
            main_game.is_gameover = True

    def bullet_hit_bullet(self,main_game):
        for each in main_game.enemy_bullet_list:
            if pygame.sprite.collide_rect(self,each):
                self.live = False
                each.live = False


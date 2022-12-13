import pygame,random
from BULLET import *


class Tank(pygame.sprite.Sprite):
    # left,top分别为距离左上角的水平，垂直距离
    def __init__(self, left, top):
        pygame.sprite.Sprite.__init__(self)
        # 获取图片surface
        self.images = {'U': pygame.image.load('images/myTank/tank_T1_0(U).png'),
                       'D': pygame.image.load('images/myTank/tank_T1_0(D).png'),
                       'L': pygame.image.load('images/myTank/tank_T1_0(L).png'),
                       'R': pygame.image.load('images/myTank/tank_T1_0(R).png')
                       }
        self.direction = 'U'
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = 5
        self.stop = True
        self.live = True

        # 记录上一次的位置
        self.lastleft = self.rect.left
        self.lasttop = self.rect.top

    def display(self,main_game):
        # 这一行是改变方向的关键，不然坦克图片不变
        self.image = self.images[self.direction]
        main_game.window.blit(self.image, self.rect)

    def shot(self):
        return Bullet(self)

    def stay(self):
        self.rect.left = self.lastleft
        self.rect.top = self.lasttop

    def hit_wall(self,main_game):
        for wall in main_game.wall_list:
            if pygame.sprite.collide_rect(self,wall):
                self.stay()

    def hit_home(self,main_game):
        if pygame.sprite.collide_rect(self, main_game.my_home):
            self.stay()

class myTank(Tank):
    def __init__(self,left,top,player):
        super(myTank,self).__init__(left,top)
        if player == 1:
            self.images = {'U': pygame.image.load('images/myTank/tank_T1_0(U).png'),
                           'D': pygame.image.load('images/myTank/tank_T1_0(D).png'),
                           'L': pygame.image.load('images/myTank/tank_T1_0(L).png'),
                           'R': pygame.image.load('images/myTank/tank_T1_0(R).png')
                           }
        elif player == 2:
            self.images = {'U': pygame.image.load('images/myTank/tank_T2_0(U).png'),
                           'D': pygame.image.load('images/myTank/tank_T2_0(D).png'),
                           'L': pygame.image.load('images/myTank/tank_T2_0(L).png'),
                           'R': pygame.image.load('images/myTank/tank_T2_0(R).png')
                           }
        if player == 1:
            self.rect.left, self.rect.top = 3 + 24 * 8, 3 + 24 * 24
        elif player == 2:
            self.rect.left, self.rect.top = 3 + 24 * 16, 3 + 24 * 24

    def hit_othertank(self,main_game):
        for enemy in main_game.enemytank_list:
            if pygame.sprite.collide_rect(self,enemy):
                self.stay()

        main_game.ourtank_list.remove(self)
        if main_game.ourtank_list:
            for other in main_game.ourtank_list:
                if pygame.sprite.collide_rect(self, other):
                    self.stay()
        main_game.ourtank_list.append(self)

    def move(self):
        self.lastleft = self.rect.left
        self.lasttop = self.rect.top
        if self.direction == 'L':
            if self.rect.left>0:
                self.rect.left -= self.speed
        elif self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'R':
            if self.rect.left < 630-self.rect.height:
                self.rect.left += self.speed
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < 630 :
                self.rect.top += self.speed


class enemyTank(Tank):
    def __init__(self,left,top,speed,x=None):
        super(enemyTank, self).__init__(left,top)

        # 用于给刚生成的坦克播放出生特效
        self.born = True
        self.times = 50
        self.level = random.randint(0,3)
        self.hp =  1
        self.images = [
                    {'U': pygame.image.load('images/enemyTank/enemy_1_0(U).png'),
                     'D': pygame.image.load('images/enemyTank/enemy_1_0(D).png'),
                     'L': pygame.image.load('images/enemyTank/enemy_1_0(L).png'),
                     'R': pygame.image.load('images/enemyTank/enemy_1_0(R).png')
                     },
                    {'U': pygame.image.load('images/enemyTank/enemy_2_1(U).png'),
                     'D': pygame.image.load('images/enemyTank/enemy_2_1(D).png'),
                     'L': pygame.image.load('images/enemyTank/enemy_2_1(L).png'),
                     'R': pygame.image.load('images/enemyTank/enemy_2_1(R).png')
                     },
                    {'U': pygame.image.load('images/enemyTank/enemy_3_3(U).png'),
                     'D': pygame.image.load('images/enemyTank/enemy_3_3(D).png'),
                     'L': pygame.image.load('images/enemyTank/enemy_3_3(L).png'),
                     'R': pygame.image.load('images/enemyTank/enemy_3_3(R).png')
                     },
                    {'U': pygame.image.load('images/enemyTank/enemy_4_2(U).png'),
                     'D': pygame.image.load('images/enemyTank/enemy_4_2(D).png'),
                     'L': pygame.image.load('images/enemyTank/enemy_4_2(L).png'),
                     'R': pygame.image.load('images/enemyTank/enemy_4_2(R).png')
                     }
                       ]

        self.direction = self.rand_direction()
        self.image = self.images[self.level][self.direction]
        self.rect = self.image.get_rect()
        # 坦克位置
        if x is None:
            self.x = random.randint(0, 2)
        else:
            self.x = x
        self.rect.left, self.rect.top = 3 + self.x * 12 * 24, 3
        self.speed = speed+self.level*0.5
        self.stop = True
        self.step = 100

    def rand_direction(self):
        num = random.randint(1,8)
        # 使向下的可能性变高
        if num ==1:
            return 'U'
        elif 2<= num <=4:
            return 'D'
        elif num ==5 or num ==6:
            return 'L'
        elif num ==7 or num == 8:
            return 'R'
        # 让敌方坦克改变方向更丝滑，不会抽搐
        num = 0

    def randmove(self):
        if self.step <= 0:
            self.step = 50
            self.direction = self.rand_direction()
        else:
            self.move()
            self.step -= 1

    def shot(self):
        num = random.randint(1, 1000)
        if num <= 50+self.level*10:
            return Bullet(self)

    def display(self,main_game):
        # 这一行是改变方向的关键，不然坦克图片不变
        self.image = self.images[self.level][self.direction]
        main_game.window.blit(self.image, self.rect)

    def change_direction(self):
        directions = ['U','R','D','L']
        directions.remove(self.direction)
        num = random.randint(0,2)
        self.direction = directions[num]

    def enemy_hit_mytank(self,main_game):
        if main_game.my_tank:
            if pygame.sprite.collide_rect(self,main_game.my_tank):
                self.stay()
                self.shot()
        if main_game.your_tank:
            if pygame.sprite.collide_rect(self, main_game.your_tank):
                self.stay()
                self.shot()

    def hit_wall(self,main_game):
        for wall in main_game.wall_list:
            if pygame.sprite.collide_rect(self,wall):
                self.stay()
                self.change_direction()

    def hit_othertank(self,main_game):
        others = main_game.enemytank_list[:]
        others.remove(self)
        for tank in others:
            if pygame.sprite.collide_rect(self,tank):
                self.stay()
                self.change_direction()

    def move(self):
        self.lastleft = self.rect.left
        self.lasttop = self.rect.top
        if self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.stay()
                self.change_direction()
        elif self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                self.stay()
                self.change_direction()
        elif self.direction == 'R':
            if self.rect.left < 630 - self.rect.height:
                self.rect.left += self.speed
            else:
                self.stay()
                self.change_direction()
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < 630:
                self.rect.top += self.speed
            else:
                self.stay()
                self.change_direction()

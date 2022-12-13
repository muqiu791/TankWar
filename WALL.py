import pygame


class Wall():
    def __init__(self,left,top):
        self.image = pygame.image.load('images/scene/brick.png')
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.live = True
        # 用来记录墙壁的生命值
        self.hp = 1

    def display(self,main_game):
        main_game.window.blit(self.image,self.rect)


class Iron_wall(Wall):
    def __init__(self,left,top):
        super(Iron_wall, self).__init__(left,top)
        self.image = pygame.image.load('images/scene/iron.png')
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.live = True
        self.hp = 9999

    def display(self,main_game):
        main_game.window.blit(self.image,self.rect)


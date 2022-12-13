import pygame
class Explode():
    def __init__(self,tank):
        self.images = [
            pygame.image.load('images/explode/blast0.gif'),
            pygame.image.load('images/explode/blast1.gif'),
            pygame.image.load('images/explode/blast2.gif'),
            pygame.image.load('images/explode/blast3.gif'),
            pygame.image.load('images/explode/blast4.gif'),
            pygame.image.load('images/explode/blast5.gif'),
            pygame.image.load('images/explode/blast6.gif'),
            pygame.image.load('images/explode/blast7.gif')
        ]
        self.rect = tank.rect
        self.step = 0
        self.image = self.images[self.step]
        self.live = True

    def display(self,main_game):
        if self.step < len(self.images):
            self.image = self.images[self.step]
            main_game.window.blit(self.image,self.rect)
            self.step +=1
        else:
            self.step =0
            self.live =False

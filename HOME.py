# 大本营类
import pygame


# 大本营类
class Home(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/home/home1.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (3 + 12 * 24, 3 + 24 * 24)
        self.alive = True
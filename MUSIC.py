import pygame


class Music():
    def __init__(self, filename):

        self.filename = filename
        pygame.mixer.init()
        pygame.mixer.music.load(self.filename)

    def play_music(self):
        pygame.mixer.music.play()

"""Font Class

Module responsible for displaying texts on the screen
using the `pygame.font.Font`
"""
import pygame


class Font():
    
    def __init__(self, font, size, screen):
        super(Font, self).__init__()
        self.font_family = font
        self.size = size
        self.color = (0,0,0)
        self.background = None
        self.screen = screen
        self.font = pygame.font.Font(self.font_family, self.size)

    def load(self, text):
        self.text = text
        self.font_rendered = self.font.render(self.text, True, self.color, self.background)
        return self.font_rendered

    def renderize(self, text, position):
        self.position = position
        self.screen.blit(self.load(text), self.position)
        
        
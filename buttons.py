import pygame
from pygame.locals import *

class Button:
    '''
    Class to handle GUI type buttons.
    '''

    def __init__(self, parent, pos = (0, 0), id = 'btn', img = None, callback = None):
        '''
        id - (string) id of button, passed back to callback
        img - (pygame.image) image for button, otherwise you just get a 60x25 dark grey rectangle
        callback - function to call when button is clicked.  includes the id as parameter.
        '''
        self.parent = parent
        self.x, self.y = pos

        self.image = img
        if not img:
            self.image = pygame.Surface((60, 25))
            self.image.fill((200, 200, 200))
        
        self.rect = pygame.Rect((self.x, self.y), self.image.get_size())
        self.tip = 'Click me'
        self.down_click = False
        self.id = id
        self._callback = callback

    def set_callback(self, callback = None):
        '''
        omit parameter to set to None
        '''
        self._callback = callback
        
    def get_size(self):
        return (self.image.get_width(), self.image.get_height())

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()
    
    def check_mouse(self, pos):
        return self.rect.collidepoint(pos)

    def update(self):
        pass

    def on_click(self):
        if self._callback:
            self._callback(self.id)
        else:
            print ('clicked: [{}] - '.format(self.id))


    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

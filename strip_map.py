import pygame
from sprite import *
from helpers import *

class Strip_Map:

    def __init__(self, x, y, filename):

        self.x = x
        self.y = y
        self.load_strip(filename)

    def get_frame(self, index):
        return self.sprite_strip.get_frame(index)

    def load_strip(self, filename):

        self.image = load_file(filename)

        if self.image:        
            self.image2x = pygame.transform.scale2x(self.image)
            self.rect = pygame.Rect((self.x, self.y), self.image.get_size())
            self.rect2x = pygame.Rect(self.x + self.rect.width + 10, self.y, self.rect.width * 2, self.rect.height * 2)

            # image, rect, count, colorkey=None, loop=False, frames=1
            self.sprite_strip = SpriteStripAnim(self.image, (0,0,16,16), 16, colorkey = (255,0,255))
            self.selected_cell = 0
            self.selected_rect = pygame.Rect(self.x, self.y, 16, 16)
            self.selected_rect2x = pygame.Rect(self.rect.x + self.rect.width + 20,self.y, 32, 32)

            return True 
        else:
            return False

    def check_click(self, pos):
        return self.rect.collidepoint(pos) or self.rect2x.collidepoint(pos)

    def handle_click(self, pos):
        x, y = pos

        if self.rect.collidepoint(pos):
            self.selected_cell = (y - self.y) // 16
            
        elif self.rect2x.collidepoint(pos):
            self.selected_cell = (y - self.y) // 32
            
        self.selected_rect.y = self.y + self.selected_cell * 16
        self.selected_rect2x.y = self.y + self.selected_cell * 32
        
        return self.get_frame(self.selected_cell)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        pygame.draw.rect(surface, (255,255,0), self.selected_rect, 2)

        surface.blit(self.image2x, (self.x + self.rect.width + 20, self.y))
        pygame.draw.rect(surface, (255,255,0), self.selected_rect2x, 4)

        



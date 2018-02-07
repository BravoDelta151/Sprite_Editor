import pygame
from sprite import *
from helpers import *
from buttons import *

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
        selected_cell = self.selected_cell

        if self.rect.collidepoint(pos):
            self.selected_cell = (y - self.y) // 16
            
        elif self.rect2x.collidepoint(pos):
            self.selected_cell = (y - self.y) // 32
            
        self.selected_rect.y = self.y + self.selected_cell * 16
        self.selected_rect2x.y = self.y + self.selected_cell * 32
        
        return self.get_frame(self.selected_cell), selected_cell != self.selected_cell

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        pygame.draw.rect(surface, (255,255,0), self.selected_rect, 2)

        surface.blit(self.image2x, (self.x + self.rect.width + 20, self.y))
        pygame.draw.rect(surface, (255,255,0), self.selected_rect2x, 4)

class Anim_Panel:
    def __init__(self, parent, x, y, width, height, size = 128):
        self.parent = parent
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.size = size

        self.panel = pygame.Surface((self.width, self.height))
        self.panel.fill((100,100,100))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # control buttons
        self.buttons = []
        sx, sy = self.x + (self.width // 2 - 110), self.y + 10
        # parent, pos = (0, 0), id = 'btn', img = None, callback = None):
        self.buttons.append(Button(self, (sx, sy), id = "pause", callback = self._handle_button,
            img = load_file(get_dir_path("images", "pause_btn.png")).convert()))
        sx += self.buttons[-1].get_width() + 10

        self.buttons.append(Button(self, (sx, sy), id = "play", callback = self._handle_button,
            img = load_file(get_dir_path("images", "play_btn.png")).convert()))
        sx += self.buttons[-1].get_width() + 10

        self.buttons.append(Button(self, (sx, sy), id = "dec", callback = self._handle_button,
            img = load_file(get_dir_path("images", "dec_btn.png")).convert()))
        sx += self.buttons[-1].get_width() + 10

        self.buttons.append(Button(self, (sx, sy), id = "inc", callback = self._handle_button,
            img = load_file(get_dir_path("images", "inc_btn.png")).convert()))
        sx += self.buttons[-1].get_width() + 10

        self.buttons.append(Button(self, (sx, sy), id = "fr14", callback = self._handle_button,
            img = load_file(get_dir_path("images", "fr14_btn.png")).convert()))
        sx += self.buttons[-1].get_width() + 10

        self.buttons.append(Button(self, (sx, sy), id = "fr28", callback = self._handle_button,
            img = load_file(get_dir_path("images", "fr28_btn.png")).convert()))
        sx += self.buttons[-1].get_width() + 10


        # view port
        self.view_port = pygame.Surface((self.size, self.size))
        sx = self.x + (self.width // 2 - self.size // 2)
        sy = self.y + self.buttons[-1].get_height() + (self.height // 2 - self.size // 2)
        
        self.view_rect = pygame.Rect(sx, sy, self.size, self.size)

        self.dirty = False

    def _handle_button(self, id):
        print("Tile _handle_button called - {}".format(id))
        if id == "pause":
            pass
        elif id == "play":
            pass
        elif id == "dec":
            pass
        elif id == "inc":
            pass
        elif id == "fr14":
            pass
        elif id == "fr28":
            pass
    
    def _update(self):
        if self.dirty:
            pass

    def handle_click(self, pos, btn):
        for b in self.buttons:
            if b.check_mouse(pos):
                b.on_click()
                break

    def draw(self, surface):
        self._update()
        surface.blit(self.panel, (self.x, self.y))

        for b in self.buttons:
            b.draw(surface)

        surface.blit(self.view_port, self.view_rect.topleft)
        pygame.draw.rect(surface, (255,255,255), self.rect, 2)

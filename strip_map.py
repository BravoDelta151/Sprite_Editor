import pygame
from sprite import *
from helpers import *
from components import *

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

    def update(self, image):
        
        if image.get_size() == self.selected_rect.size:
            # print("Strip_Map: update: {}".format(image))
            sy = self.selected_cell * 16
            for x in range(image.get_width()):
                for y in range(image.get_height()):
                    color = image.get_at((x,y))
                    self.image.set_at((x, sy + y), color)
            self.image2x = pygame.transform.scale2x(self.image)
            # self.image.blit(image, self.selected_rect.topleft)
            self.sprite_strip.update_cell(image, self.selected_cell)
        else:
            print("Strip_Map: update - size mismatch {} != {} ".format(image.get_size(), self.selected_rect.size))

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
        pygame.draw.rect(surface, (255,255,0), self.selected_rect, 1)

        surface.blit(self.image2x, (self.x + self.rect.width + 20, self.y))
        pygame.draw.rect(surface, (255,255,0), self.selected_rect2x, 2)

class Anim_Panel:
    '''
    Adds a panel to preview animations.  
    > Right click on a cell in the main strip view to add that cell.  You can add the same cell muliple times
    > Play/Pause are self explanatory.  When playing, the frame_rate and frame number will be displayed
    > + and - buttons increment and decrement the frame_rate  !!! NOT YET IMPLEMENTED
    > 14 and 28 buttons set frame_rate to respective number   !!! NOT YET IMPLEMENTED
    > Red X clears the image strip
    '''
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
        sx, sy = self.x + (self.width // 2 - 125), self.y + 10
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

        self.buttons.append(Button(self, (sx, sy), id = "clear", callback = self._handle_button,
            img = load_file(get_dir_path("images", "x_btn.png")).convert()))
        sx += self.buttons[-1].get_width() + 10
        
        self.strip_rect = pygame.Rect((self.buttons[0].left, self.y + self.buttons[-1].get_height() + 20, 16, 256))
        self.text_pos = pygame.Rect(self.strip_rect.right + 20, self.strip_rect.top, 200, 16)

        # view port
        self.view_port = pygame.Surface((self.size, self.size))
        self.view_port.fill((100,100,100))

        sx = self.x + (self.width // 2 - self.size // 2)
        sy = self.y + self.buttons[-1].get_height() + (self.height // 2 - self.size // 2)
        self.frame_rate = 14
        self.sprite = Sprite(None, sx, sy, 16,16, 0, frame_rate = self.frame_rate)
        
        self.view_rect = pygame.Rect(sx, sy, self.size, self.size)

        self._frame_number = -1
        self.paused = True
        self.dirty = False

    def _handle_button(self, id):
        if id == "pause":
            self.paused = True
        elif id == "play":
            self.paused = self.sprite.strip.count <=  0
            if not self.paused:
                self.sprite.strip.iter()
        elif id == "clear":
            self.reset()
        elif id == "dec":
            print("Anim_ _handle_button called - {}".format(id))
        elif id == "inc":
            print("Anim_ _handle_button called - {}".format(id))
        elif id == "fr14":
            print("Anim_ _handle_button called - {}".format(id))
        elif id == "fr28":
            print("Anim_ _handle_button called - {}".format(id))
        
    
    def _update(self):
        if self.sprite.strip.count > 0:            
            if not self.paused:
                image = self.sprite.strip.next()  
                self._frame_number = self.sprite.strip.current_frame              
            else:
                image = self.sprite.strip.get_frame(-1)
                self._frame_number = -1

            if image:
                pygame.transform.scale(image, self.view_rect.size, self.view_port)
                self.view_port.set_colorkey((255,0,255))

        if self.dirty:
            pass

    def reset(self):
        self.paused = True
        self.sprite.strip.delete_cell()
        self.view_port.fill((100,100,100))
        self._frame_number = -1

    def add_cell(self, image):
        '''
        adds cell to the strip to animate
        '''        
        self.sprite.strip.add_cell(image)

    def handle_click(self, pos, btn):
        for b in self.buttons:
            if b.check_mouse(pos):
                b.on_click()
                break

    def _draw_text(self, surface):
        if not self.paused and self._frame_number >= 0:
            font = pygame.font.Font(None, 24)
            line0 = font.render("Frame Rate: {}".format(self.frame_rate), 1, (255,0,0))
            line1 = font.render("Frame Number: {}".format(self._frame_number), 1, (255,0,0))
            surface.blit(line0, self.text_pos.topleft)
            surface.blit(line1, (self.text_pos.left, self.text_pos.top + line0.get_height() + 3))
            


    def draw(self, surface):
        self._update()
        surface.blit(self.panel, (self.x, self.y))

        for b in self.buttons:
            b.draw(surface)
        
        for i in range(self.sprite.strip.count):
            surface.blit(self.sprite.strip.get_frame(i), (self.strip_rect.left, self.strip_rect.top + (i * 16)))

        surface.blit(self.view_port, self.view_rect.topleft)
        
        self._draw_text(surface)
            

        pygame.draw.rect(surface, (255,255,255), self.rect, 2)

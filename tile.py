import pygame
import os
from helpers import *


class Pixel:
    '''
    This class handles a single pixel in the bitmap and shows it as a block in the
    tile editor
    '''
    def __init__(self, parent, x, y, size, color = None, colorkey = (255,0,255,255)):
        '''
        '''
        self.parent = parent
        self.x = x
        self.y = y
        self.size = size

        self.rect = pygame.Rect(x,y, size, size)
        self.color = color
        self.colorkey = colorkey

        self.image = pygame.Surface((size, size))

        if self.color:
            self.image.fill(self.color)            
        else:
            self._draw_cross()
            
    def get_color(self):
        '''
        Gets current color of pixel block
        '''
        if self.color:
            return self.color 
        elif self.colorkey:
            return self.colorkey
        else:
            return (255,0,255, 255)
        
    def _draw_cross(self):
        '''
        Draw a black box with a cross inside to indicate a transparent pixel
        '''
        light_grey = (150,150,150,255)
        dark_grey = (75,75,75, 255)
        if self.x >= 512 or self.y >= 512:
            self.image.fill((255,0,0,255))
        else:
            self.image.fill(dark_grey)

        half = self.size // 2
        q = 4
        # pygame.draw.line(self.image, (100,100,100), (self.x + q, self.y + half), (self.size - q, self.y + half), 1)
        # pygame.draw.line(self.image, (100,100,100), (self.x + half, self.y + q), (self.x + half, self.size - q), 1)
        pygame.draw.line(self.image, light_grey, (q, half), (self.size - q, half), 1)
        pygame.draw.line(self.image, light_grey, (half, q), (half, self.size - q), 1)
        pygame.draw.rect(self.image, light_grey, (0,0,self.size, self.size), 1)

    def set(self, color):
        '''
        Sets the color or calls draw cross for transparent pixels
        '''
        # print(color)
        if not self.color or self.color != color:
            self.parent.dirty = True
            if not color or (self.colorkey and color == self.colorkey):
                self._draw_cross()
                self.color = None
            else:
                self.image.fill(color)
                pygame.draw.rect(self.image, (100,100,100), (0,0,self.size, self.size), 1)
                self.color = color

    def check_pos(self, pos):
        '''
        check for mouseclick
        '''
        return self.rect.collidepoint(pos)


    def draw(self, surface):
        '''
        draws on surface parameter
        '''    
        surface.blit(self.image, (self.x, self.y))
        

class Tile_Editor:

    def __init__(self, x, y, width, height, palette, image = None, show_grid = True):
        self.x = x
        self.y = y

        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

        self.palette = palette

        self.image = image
        if not self.image:
            self.image = pygame.Surface((width, height))
            self.image.fill((100,100,100))

        self.img = pygame.Surface((16,16)).convert()
        self.img.set_colorkey((255,0,255), pygame.RLEACCEL)

        pix_size = width // 16
        # x, y, size
        self.pixels = [[Pixel(self, x * pix_size ,y * pix_size ,pix_size) for y in range(pix_size)] for x in range(pix_size)]
        self.pixel_size = pix_size

        sx = self.x + self.width + 10
        sy =self.y 
        self.brush_btn = load_file(get_dir_path("images", "brush_btn.png")).convert()
        self.brush_btn_rect = pygame.Rect((sx, sy), self.brush_btn.get_size())

        sy += self.brush_btn.get_height() + 10
        self.fill_btn = load_file(get_dir_path("images", "fill_btn.png")).convert()
        self.fill_btn_rect = pygame.Rect((sx, sy), self.brush_btn.get_size())
        sy += self.fill_btn.get_height() + 10

        self.grid = load_file(get_dir_path("images", "grid.png")).convert()
        sw, sh = self.grid.get_size()
        self.grid_rect = pygame.Rect(sx, sy, sw, sh)

        sy += sh + 10
        self.gridx2 = pygame.transform.scale2x(self.grid)
        self.gridx2_rect = pygame.Rect(sx, sy, sw, sh)

        ###############
                    
        ##############
        self.show_actual_size = True
        self.show_double_size = True
        self.dirty = True

    def _update(self):
        '''
        Checks if any changes were made and updates the image before blitting
        '''
        if self.dirty:
            l = len(self.pixels)
            for x in range(l):
                for y in range(l):
                    self.pixels[x][y].draw(self.image)
                    self.img.set_at((x,y), self.pixels[x][y].get_color())
            self.dirty = False

    def _check_pixels_pos(self, pos):
        '''
        Checks if mouse click occurred in the editor
        '''
        l = len(self.pixels)

        for x in range(l):
            for y in range(l):
                if self.pixels[x][y].check_pos(pos):
                    return x, y
        return -1, -1

    def set_image(self,image):
        if image:
            # l = self.pixel_size # len(self.pixels)
            # print('set_image: image size = {} <> {}'.format(image.get_size(), l))
            w, h = image.get_size()
            self.img = image
            for x in range(w):
                for y in range(h):
                    color = image.get_at((x,y))
                    # print('{}, {} - {}'.format(x,y, color))
                    self.pixels[x][y].set(color)
            self.dirty = True

    def handle_click(self, pos, button):
        '''
        Handles mouse clicks
        '''
        if self.rect.collidepoint(pos):
            button = button or 0
            px, py = pos

            # print("Tile Editor clicked")
            x, y = self._check_pixels_pos((px - self.x, py - self.y))
            if x >= 0 and y >= 0:
                color = self.palette.get_color(button)
                self.pixels[x][y].set(color)

        elif self.brush_btn_rect.collidepoint(pos):
            print("brush btn clicked")

        elif self.fill_btn_rect.collidepoint(pos):
            print("fill btn clicked")

    def draw(self, surface):
        '''
        handles drawing the tile editor, previe boxes and fill/brush buttons
        '''
        self._update()
        # image = self.pixel_array.make_surface()
        pygame.draw.rect(surface, (100,100,100), (self.x - 1, self.y - 1, self.width + 1, self.height + 1), 4)
        surface.blit(self.image, (self.x, self.y))

        surface.blit(self.brush_btn, self.brush_btn_rect.topleft)

        surface.blit(self.fill_btn, self.fill_btn_rect.topleft)

        
        if self.show_actual_size:
            surface.blit(self.grid, self.grid_rect.topleft)
            surface.blit(self.img, self.grid_rect.topleft)
        if self.show_double_size:
            i2x = pygame.transform.scale2x(self.img)
            # i2x.set_colorkey((255,0,255), pygame.RLEACCEL)
            surface.blit(self.gridx2,self.gridx2_rect.topleft)
            surface.blit(i2x,self.gridx2_rect.topleft)
            # surface.blit(pygame.transform.scale2x(i2x), (sx, sy + 74))
        # if self.show_grid:
        #     surface.blit(self.grid, (self.x, self.y))
        # pygame.draw.rect(surface, (0,0,0), (self.x - 1, self.y - 1, self.width + 1, self.height + 1), 2)


class Palette:
    '''
    The palette class creates a menu of selectable colors to choose from.  the default is the NES palette
    '''
    def __init__(self, palette = None):
        
        self.palette = palette

        if not self.palette:
            print("Using Default Palette:")
            self.palette = [ (124,124,124), (0,0,252), (0,0,188), (68,40,188), (148,0,132), (168,0,32), (168,16,0), (136,20,0), 
                (80,48,0), (0,120,0), (0,104,0), (0,88,0), (0,64,88), (0,0,0), (0,0,0), (0,0,0), (188,188,188), (0,120,248), 
                (0,88,248), (104,68,252), (216,0,204), (228,0,88), (248,56,0), (228,92,16), (172,124,0), (0,184,0), (0,168,0), 
                (0,168,68), (0,136,136), (0,0,0), (0,0,0), (0,0,0), (248,248,248), (60,188,252), (104,136,252), (152,120,248), 
                (248,120,248), (248,88,152), (248,120,88), (252,160,68), (248,184,0), (184,248,24), (88,216,84), (88,248,152),
                (0,232,216), (120,120,120), (0,0,0), (0,0,0), (252,252,252), (164,228,252), (184,184,248), (216,184,248), 
                (248,184,248), (248,164,192), (240,208,176), (252,224,168), (248,216,120), (216,248,120), (184,248,184), 
                (184,248,216), (0,252,252), (248,216,248), (0,0,0), (0,0,0) ]
        
        self.blocks = [ {'surf': pygame.Surface((16,16)), 
                        'rect': pygame.Rect((0, 0, 16,16)) } for _ in range(len(self.palette)) ]

        # self.blocks.surf = [pygame.Surface((16,16)) for _ in range(len(self.palette))]
        self.x, self.y = 0, 0

        for index, tup in enumerate(self.palette):            
            color = pygame.Color(tup[0], tup[1], tup[2], 0)
            # print(len(self.blocks))
            self.blocks[index]['surf'].fill(color)

        # left_color is for the left mouse button == 1
        self.left_color = pygame.Surface((31, 31))
        self.left_color.fill(pygame.Color(0,0,0, 255))

        # right_color is for the right mouse button == 3
        self.right_color = pygame.Surface((31, 31))
        self.right_color.fill(pygame.Color(255,255,255, 255))

    @classmethod
    def init_from_file(cls, filename):
        '''
        call this to initialize with a defined paletted file.  Palette must contain exactly 64 
        defined colors.
        '''
        lines = None
        data = []
        with open(filename) as f:
            lines = f.read().splitlines()
        for line in lines:
            values = line.split(',')
            if len(values) != 3:
                print ('{} -- {}'.format(line, values))
                data.append((255,255,255))
            else:
                data.append((int(values[0]), int(values[1]), int(values[2])))
        return cls(data)

    def handle_click(self, pos, button):
        '''
        Handle mouse click 
        '''
        for b in self.blocks:
            if b['rect'].collidepoint(pos):
                if button == 1:
                    self.left_color.fill(b['surf'].get_at((8,8)))
                elif button == 3:
                    self.right_color.fill(b['surf'].get_at((8,8)))
                return True
        return False

    def get_color(self, button):
        '''
        Get desire color based on which mouse button was clicked
        '''
        if button and button == 1:
            return self.left_color.get_at((8,8))
        elif button and button == 3:
            return self.right_color.get_at((8,8))
        else:
            return (255,0,255)


    def draw(self, surface, pos):
        '''
        Handles drawing palette
        '''
        sx, sy = pos
        bUpdate = False
        if self.x != sx and self.y != sy:
            bUpdate = True
            self.x = sx
            self.y = sy
        
        surface.blit(self.left_color, pos)
        surface.blit(self.right_color, (sx, sy + 33))

        # rect(Surface, color, Rect, width=0)
        # Add a rectangle around the buttons for decoration
        pygame.draw.rect(surface, (255,255,255), (sx, sy, 31, 31), 2)
        pygame.draw.rect(surface, (0,0,0), (sx, sy + 33, 31, 31), 2)
        count = 1
        sx += 36

        # this draws each color
        for b in self.blocks:
            surface.blit(b['surf'], (sx, sy))
            if bUpdate:
                b['rect'].x = sx
                b['rect'].y = sy
            if count == 16:
                sx, j = pos
                sx += 36
                sy += 16
                count = 1
            else:
                sx += 16
                count += 1
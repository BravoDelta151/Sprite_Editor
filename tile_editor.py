import pygame
import os
from helpers import *
from components import *


class Palette:
    '''
    The palette class creates a menu of selectable colors to choose from.  the default is the NES palette
    TODO: Add colors from image if not in paletted already

    TODO: Add ability to create custom colors and save custom palettes

    '''
    def __init__(self, palette = None):
        
        self.palette = palette

        # Default Pallette
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
                # print ('{} -- {}'.format(line, values))
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



class Pixel:
    '''
    This class handles a single pixel in the bitmap and shows it as a block in the
    tile editor

    TODO: add option to select how a transparent pixel is displayed
    '''
    def __init__(self, parent, x, y, size, color = None, colorkey = (255,0,255,255)):
        '''
        parent, x, y, 
        size (pixels are square)
        color (initial color to set)
        '''
        self.parent = parent
        self.x = x
        self.y = y
        self.size = size

        self.rect = pygame.Rect(x,y, size, size)
        self.color = color
        self.orig_color = color
        self.colorkey = colorkey

        self.image = pygame.Surface((size, size))

        if self.color:
            self.image.fill(self.color)            
        else:
            self._draw_transparent()

        self._changed = False


    @property
    def changed(self):
        return self._changed or self.color != self.orig_color


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


    def _draw_transparent(self):
        '''
        TODO: add other ways of indicating a transparent pixel...
        '''
        self._draw_cross()


    def _draw_cross(self):
        '''
        Draw a dark box with a crosshair inside to indicate a transparent pixel
        '''
        light_grey = (150,150,150,255)
        dark_grey = (75,75,75, 255)
        if self.x >= 512 or self.y >= 512:
            self.image.fill((255,0,0,255))
        else:
            self.image.fill(dark_grey)

        half = self.size // 2
        q = 4
        pygame.draw.line(self.image, light_grey, (q, half), (self.size - q, half), 1)
        pygame.draw.line(self.image, light_grey, (half, q), (half, self.size - q), 1)
        pygame.draw.rect(self.image, light_grey, (0,0,self.size, self.size), 1)


    def set(self, color):
        '''
        Sets the color or calls draw cross for transparent pixels
        '''
        # print(color)
        if not self.color or self.color != color:
            self.parent.set_dirty()
            if not color or (self.colorkey and color == self.colorkey):
                self._draw_transparent()
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
    '''
    Creates a grid of Pixels to display a 16 x 16 image
    > Brush - can change one pixel at a time (NOTE: Must click on each pixel) 
        cursor is a broken x
    > Fill - fill region, cursor changes to a diamond
    > Load - load a bank
    > New - create a new bank
    > Update - Updates the cell with changes made in Pixels. Outlined in red if a change is detected.
        NOTE: If you don't click this all changes are lost if you switch to another cell
    > Save - saves current bank, should prompt for filename if untitled
    > Save As - Saves a new bank only, 
    '''

    def __init__(self, parent, x, y, width, height, palette, image = None):
        '''
        parent, x, y, width, height, palette, image = None
        '''
        self.x, self.y = x, y        
        self.width, self.height = width, height
        self.parent = parent
        self.palette = palette

        self.rect = pygame.Rect(x, y, width, height)

        self.image = image
        if not self.image:
            self.image = pygame.Surface((width, height))
            self.image.fill((100,100,100))

        self.preview = pygame.Surface((16,16)).convert()
        self.preview.set_colorkey((255,0,255), pygame.RLEACCEL)

        self._copy_paste = pygame.Surface((16,16)).convert()
        self._copy_paste.set_colorkey((255,0,255,255), pygame.RLEACCEL)

        pix_size = width // 16
        # x, y, size
        self.pixels = [[Pixel(self, x * pix_size ,y * pix_size ,pix_size) for y in range(pix_size)] for x in range(pix_size)]
        self.pixel_size = pix_size

        self.buttons = []
        # parent, pos = (0, 0), id = 'btn', key = "not-set", img = None
        # add brush button and fill button
        # sx, sy - button position variables
        sx = self.x + self.width + 10
        sy =self.y 
        

        self.buttons.append(Button(self, (sx,sy), id = "brush", callback = self._handle_button,
            img = load_image(get_dir_path("images", "brush_btn.png")).convert()))
        sy += self.buttons[-1].get_height() + 10

        self.buttons.append(Button(self, (sx,sy), id = "fill", callback = self._handle_button,
            img = load_image(get_dir_path("images", "fill_btn.png")).convert()))
        sy += self.buttons[-1].get_height() + 10
        self._cursor_bottom = sy - 5

        sy += 10
        # Add Load and new buttons
        # width, height, bg_color = (255,255,255), label = ''
        # btn_img = create_button_image(50, 25, label = "Load", font_size = 24) 
        self.buttons.append(Button(self, (sx,sy), id = "load", callback = self._handle_button,
            img = load_image(get_dir_path("images", "load_btn.png")).convert()))

        sy += self.buttons[-1].get_height() + 10

        self.buttons.append(Button(self, (sx,sy), id = "new", callback = self._handle_button,
            img = load_image(get_dir_path("images", "new_btn.png")).convert()))
        sy += self.buttons[-1].get_height() + 10

        self.buttons.append(Button(self, (sx,sy), id = "update", callback = self._handle_button,
            img = load_image(get_dir_path("images", "update_btn.png")).convert()))
        sy += self.buttons[-1].get_height() + 10

        # self.auto_update_cb = Check_Box(sx +10, sy - 5, id="auto_update", label = "Auto Update", 
        #     img = load_image(get_dir_path("images", "cb_open.png")),
        #     img_selected = load_image(get_dir_path("images", "cb_selected.png")),
        #     callback = self._handle_checkbox)
        # sy += self.auto_update_cb.get_height() + 5
        
        # Add save buttons
        self.buttons.append(Button(self, (sx,sy), id = "save", callback = self._handle_button,
            img = load_image(get_dir_path("images", "save_btn.png")).convert()))
        sy += self.buttons[-1].get_height() + 10

        self.buttons.append(Button(self, (sx,sy), id = "saveas", callback = self._handle_button,
            img = load_image(get_dir_path("images", "saveas_btn.png")).convert()))
        sy += self.buttons[-1].get_height() + 10

        # Add grid and 2x grid backgrounds
        # TODO: Consider adding button to hide grid 
        self.grid = load_image(get_dir_path("images", "grid.png")).convert()
        sw, sh = self.grid.get_size()
        self.grid_rect = pygame.Rect(sx, sy, sw, sh)

        sy += sh + 10
        self.gridx2 = pygame.transform.scale2x(self.grid)
        self.gridx2_rect = pygame.Rect(sx, sy, sw, sh)

        sy += (sh * 2) + 10
        self.copy_btn = Button(self, (sx,sy), id = "copy", callback = self._handle_button,
            img = load_image(get_dir_path("images", "copy_btn.png")).convert())      
        self.paste_btn = Button(self, (sx,sy), id = "paste", callback = self._handle_button,
            img = load_image(get_dir_path("images", "paste_btn.png")).convert())
        self.paste_btn.set_enabled(False)

        self.buttons.append(self.copy_btn)
        self.buttons.append(self.paste_btn)

        self._right = sx + self.buttons[-1].get_width()
        
        # options to show/hide previews 
        self.show_actual_size = True
        self.show_double_size = True

        self.auto_update = False
        self._mode = 'brush'
        self._cursor = pygame.cursors.broken_x
        # dirty flag to determine if img needs updated
        self.dirty = True

        # changed flag to detect if any changes occurred
        self.changed = False

        self._not_ready = ["save", ""]


    @property
    def cursor(self):
        return self._cursor


    @property
    def right(self):
        return self._right


    def set_dirty(self, dirty = True):
        self.dirty = dirty
        if dirty:
            self.changed = True


    def _update(self):
        '''
        Checks if any changes were made and updates the image before blitting
        '''
        if self.dirty:
            l = len(self.pixels)
            for x in range(l):
                for y in range(l):
                    self.pixels[x][y].draw(self.image)
                    self.preview.set_at((x,y), self.pixels[x][y].get_color())
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
        '''
        sets pixels to image
        '''
        if self.changed:
            pass
        # if self.auto_update:
        #     self._handle_button("update")
        
        if image:
            image.lock() 
            w, h = image.get_size()
            for x in range(w):
                for y in range(h):
                    color = image.get_at((x,y))
                    self.pixels[x][y].set(color)
            self.dirty = True
            self.changed = False
        
            image.unlock()


    def _handle_checkbox(self, id, selected):
        if id == "auto_update":
            self.auto_update = selected


    def _fill(self, pos, check, color, caller = None):
        x, y = pos
        neighbors = [(x, y - 1), (x - 1, y), (x, y + 1), (x+ 1, y)]
        if x >= 0 and x < 16 and y >= 0 and y < 16:
            self.pixels[x][y].set(color)
            for n in neighbors:
                if n != caller:
                    nx, ny = n
                    if self.pixels[nx][ny].get_color() == check:
                        self._fill(n, check, color, pos)


    def _handle_button(self, id):
        '''
        callback handler for all buttons
        '''        
        if id == "load":
            self.parent.load_prompt()
            self.changed = False
        elif id == "new":
            self.parent._load_bank("16x256")
            self.changed = False
        elif id == "update":
            self.dirty = True
            self._update()
            self.parent.strip_map.update(self.preview)
            self.changed = False
        elif id == "save":
            self.parent._save_bank(self.parent._display_name, True) 
        elif id == "saveas":
            self.parent.save_prompt()
        elif id == "brush":
            self._mode = 'brush'
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
            self._cursor = pygame.cursors.broken_x
        elif id == "fill":
            self._mode = 'fill'
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
            self._cursor = pygame.cursors.diamond
        elif id == "copy" or id == "paste":
            self._handle_copy_paste(id)


    def _handle_copy_paste(self, id):
        if id == "copy":
            self._copy_paste.lock()
            self.preview.lock()

        for x in range(16):
            for y in range(16):
                if id == "copy":
                    color = self.preview.get_at((x,y))
                    self._copy_paste.set_at((x,y), color)  
                else:
                    self.set_image(self._copy_paste)      
                    self._handle_button("update")
        
        if id == "copy":
            self._copy_paste.unlock()
            self.preview.unlock()

        # swap buttons
        for b in self.buttons:
            if b.id == "copy" or b.id == "paste":
                b.set_enabled(id != b.id)      


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
                if self._mode == 'fill':
                    check = self.pixels[x][y].get_color()
                    # print("Check = {} Color = {}".format(check, color))
                    if check != color:
                        self._fill((x, y), check, color)
                else:
                    self.pixels[x][y].set(color)
                
        # elif self.auto_update_cb.check_mouse(pos):
        #     self.auto_update_cb.on_click()
        else:
            for b in self.buttons:
                if b.check_mousepos(pos):
                    b.on_click()                    
                    break


    def _check_button_mouseover(self, button_ids, mouse_pos):
        for b in self.buttons:
            if b.id in button_ids and b.check_mousepos(mouse_pos):
                return True
        
        return False


    def check_mouseover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        else:
            return self._check_button_mouseover(('fill', 'brush'), mouse_pos) # or self._check_button_mouseover('brush', mouse_pos))


    def draw(self, surface):
        '''
        handles drawing the tile editor, previe boxes and fill/brush buttons
        '''
        self._update()

        pygame.draw.rect(surface, (100,100,100), (self.x - 1, self.y - 1, self.width + 1, self.height + 1), 4)
        surface.blit(self.image, (self.x, self.y))

        for b in self.buttons:
            b.draw(surface)
            if b.id == 'update' and self.changed:
                pygame.draw.rect(surface, (255, 0, 0), b.rect, 2)
            elif b.id == self._mode:
                # draw rect
                pygame.draw.rect(surface, (255,0,0), b.rect, 2)

        # self.auto_update_cb.draw(surface)

        if self.show_actual_size:
            surface.blit(self.grid, self.grid_rect.topleft)
            surface.blit(self.preview, self.grid_rect.topleft)
        if self.show_double_size:
            i2x = pygame.transform.scale2x(self.preview)
            surface.blit(self.gridx2,self.gridx2_rect.topleft)
            surface.blit(i2x,self.gridx2_rect.topleft)



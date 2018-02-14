'''
Contains general gui conponents

'''
import pygame
from pygame.locals import *
from helpers import *


class List_Box:
    '''
    TODO:
    '''
    pass


class Text_Box:

    def __init__(self, position = (0,0), size = (1,1), label = 'New', input_type = 'all'):
        self.position = position
        self.label = label
        self.type = input_type
        self.rect = pygame.Rect((position, size))
        self.text = ''
        self.font = pygame.font.SysFont('times new roman', 14)
        self.active = False
        self.blink_tick = pygame.time.get_ticks() + 1000
        self._cursor = True

    def _blink(self):
        ticks = pygame.time.get_ticks() 
        if self.blink_tick < ticks:
            self.blink_tick = ticks + 750
            self._cursor = not self._cursor
        return self._cursor

    def draw(self, surface):
        color = (96,96,96)
        if self.active:
            color = (255,255,255)
        pygame.draw.rect(surface, color, self.rect, 0)

        
        if self._blink():
            text = '{}_'.format(self.text)
        else:
            text = self.text

        w,h = self.font.size(self.label)
        x_offset = self.rect.left - (w+5)
        surface.blit(self.font.render(self.label, True, (0,0,0)), (x_offset, self.rect.top))
        if text:
            surface.blit(self.font.render(text, True, (0,0,0)), self.rect.topleft)



class Prompt:

    def __init__(self, surface, position, size, prompt_name = 'New Prompt', info = None, image = None):
        self.x, self.y = position
        self.name = prompt_name
        self.image = image
        self.rect = pygame.Rect((position, size))
        self.font = pygame.font.SysFont('times new roman', 16)
        self.text_boxes = []
        self.info = info
        self.valid_list = 'abcdefghijklmnopqrstuvwxyz0123456789-_.'
        self.active_box = None
        self.running = True
        self.Shift_Down = False

        bw, bh = size
        self.ok_btn = Button(self, (self.x + bw - 70, self.y + bh - 30), id = "ok", callback = self._handle_button,
            img = load_image(get_dir_path("images", "ok_btn.png")).convert())
        self.x_btn = Button(self, (self.x + bw - 35, self.y + bh - 30), id = "cancel", callback =self._handle_button,
            img = load_image(get_dir_path("images", "x_btn.png")).convert())
        
    def _handle_button(self, id):
        # print("Button handler: {}".format(id))
        if id == "cancel":
            for box in self.text_boxes:
                box.text = None

        self.running = id not in ("ok", "cancel")
    

    def run(self, surface):
        ret_vals = []
        if self.text_boxes and not self.active_box:
            self.active_box = self.text_boxes[0]
            self.active_box.active = True
        while self.running:
            self.process_events()
            self.draw(surface)
            pygame.display.flip()
        if self.text_boxes:
            for box in self.text_boxes:
                ret_vals.append(box.text)
        if len(ret_vals) > 1:
            return ret_vals
        else:
            return ret_vals[0]

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.ok_btn.check_mousepos(pos):
                    # print("Ok btn clicked")
                    self.ok_btn.on_click()
                elif self.x_btn.check_mousepos(pos):
                    # print("cancel btn clicked")
                    self.x_btn.on_click()
                else:
                    for box in self.text_boxes:
                        if box.rect.collidepoint(pos):
                            if self.active_box:
                                self.active_box.active = False
                            box.active = True
                            self.active_box = box
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.Shift_Down = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    for box in self.text_boxes:
                        box.text = None
                    self.running = False
                    break
                if self.active_box:
                    if event.key == pygame.K_BACKSPACE:
                        if self.active_box and self.active_box.text:
                            temp = ''
                            for i in range(len(self.active_box.text)-1):
                                temp += self.active_box.text[i]
                            self.active_box.text = temp
                        continue
                    if event.key == pygame.K_TAB:
                        ref = 0
                        for i in range(len(self.text_boxes)):
                            if self.text_boxes[i] is self.active_box:
                                ref = i
                        if ref+1 > len(self.text_boxes)-1:
                            self.active_box.active = False
                            self.active_box = self.text_boxes[0]
                            self.active_box.active = True
                        else:
                            self.active_box.active = False
                            self.active_box = self.text_boxes[ref+1]
                            self.active_box.active = True
                        continue
                    if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        self.Shift_Down = True
                        continue
                    if event.key == pygame.K_SPACE:
                        continue
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        self.running = False
                        break
                    else:
                        key_name = pygame.key.name(event.key).strip('[]')
                        if key_name not in self.valid_list:
                            continue
                        if self.active_box.type == 'all':
                            if self.Shift_Down and key_name.isalpha():
                                key_name = str.capitalize(key_name)
                            if self.Shift_Down and key_name == '-':
                                key_name = '_'
                            self.active_box.text += key_name
                        if key_name.isdigit() and self.active_box.type == 'num':
                            self.active_box.text += key_name

    def draw(self, surface):
        if self.image:
            pass
        else:
            pygame.draw.rect(surface, (192,192,192), self.rect, 0)
        w,h = self.font.size(self.name)
        cx, cy = self.rect.center
        surface.blit(self.font.render(self.name, True, (0,0,192)), (cx - int(w/2),self.rect.top))
        for box in self.text_boxes:
            box.draw(surface)
        if self.info:
            iw, ih = self.font.size(self.info)
            surface.blit(self.font.render(self.info, True, (0,0,192)), (self.x + 10, self.rect.bottom - ih - 10))
        if self.ok_btn:
            self.ok_btn.draw(surface)
        if self.x_btn:
            self.x_btn.draw(surface)


class Check_Box:
    
    def __init__(self, x, y, id = "cb", label = "CheckBox", img = None, img_selected = None, callback = None):
        self.x, self.y = x, y
        self.id = id
        self.image = img
        self.image_selected = img_selected

        if not self.image:
            self.image = pygame.Surface((24,24))
            self.image.fill((255, 255, 255))
        
        if not self.image_selected:
            self.image_selected = pygame.Surface((24,24))
            self.image_selected.fill((255,0,0))

        self.set_label(label)
        self.rect = pygame.Rect((self.x, self.y), self.image.get_size())
        self._callback = callback
        self._selected = False

    @property
    def checked(self):
        return self._selected

    def set_label(self, text):
        font = pygame.font.Font(None, 16)
        self.label = font.render(text, 1, (0,0,0))
       

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
        return self.image.get_height() + self.label.get_height()
    
    def check_mouse(self, pos):
        return self.rect.collidepoint(pos)

    def update(self):
        pass

    def on_click(self):
        self._selected = not self._selected
        if self._callback:
            self._callback(self.id, self._selected)
        else:
            print ('clicked: [{}] - '.format(self.id))


    def draw(self, surface):
        if self._selected:
            surface.blit(self.image_selected, (self.x, self.y))
        else:
            surface.blit(self.image, (self.x, self.y))
        # w, h = self.label.get_size()

        surface.blit(self.label, (self.x - 10, self.y + self.image.get_height() + 4))
        pygame.draw.rect(surface, (255,255,255), self.rect, 2)



class Button_Group:

    def __init__(self, parent, x, y, layout = 'row', padding = (0,0), label = None): # , layout = 'flow'):
        '''
        Layout:  row or col
        padding: (horizontal, vertical)
        '''
        self.parent= parent
        self.x, self.y = x, y

        self.layout = layout
        self.label = label

        self.pad_h, self.pad_v = padding
        self.rect = pygame.Rect(self.x, self.y, self.pad_h, self.pad_v)
        self._next_loc = (self.x + self.pad_h, self.y + self.pad_v)

        self.buttons = []

    def add_button(self, id = "btn", img = None, callback = None):
        nx, ny = self._next_loc
        button = Button(self, (nx, ny), id, img, callback)

        # calculate how the group rect size changed and set location for next button
        if self.layout == 'row':
            if len(self.buttons) == 0:
                self.rect.width = max(self.rect.width, button.width + (self.pad_h * 2))
            else:
                self.rect.width += button.width + self.pad_h
            
            self.rect.height = max(self.rect.height, button.height + (self.pad_v * 2))
            self._next_loc = (nx + button.width + self.pad_h, ny)

        else: # col
            if len(self.buttons) == 0:
                self.rect.height = max(self.rect.height, button.height + (self.pad_v * 2))
            else:
                self.rect.height += button.height + self.pad_v
            
            self.rect.width = max(self.rect.width, button.width + (self.pad_h * 2))
            self._next_loc = (nx, ny + button.height + self.pad_v)

        # add button to list
        self.buttons.append(button)


    def check_mousepos(self, pos):
        return self.rect.collidepoint(pos)

    def on_click(self, pos, btn):
        for b in self.buttons:
            if b.check_mousepos(pos):
                b.on_click()
                return True
        
        return False


    def draw(self, surface):
        '''
        Draw group, handles calling buttons draw function
        '''
        # only draw if there are buttons
        if len(self.buttons) > 0:
            # draw buttons
            for b in self.buttons:
                b.draw(surface)

            # draw rect
            pygame.draw.rect(surface, (0,0,0), self.rect, 1)

            # draw text
            if self.label:
                surface.blit(get_text_rendered(' {} '.format(self.label)), (self.x + self.pad_h, self.y))

        
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
        self.id = id
        
        self.image = img
        if not self.image:
            self._make_image()
            # self.image = pygame.Surface((60, 25))
            # self.image.fill((200, 200, 200))
        
        self._rect = pygame.Rect((self.x, self.y), self.image.get_size())
        self.tip = 'Click me'
        self.down_click = False

        self._enabled = True
        self._callback = callback

    def _make_image(self):
        # font = pygame.font.SysFont("arial", 16)
        # w, h = font.size(self.id)
        # self.image = pygame.Surface((max(25, w + 4), max(25, h + 4)))
        # self.image.fill((200,200,200))
        # self.image.blit(font.render(self.id, True, (0,0,190)), (4,4))
        # w, h = self.image.get_size()
        # pygame.draw.rect(self.image, (0,0,0), (0,0,w,h), 1)
        pass

    @property
    def topleft(self):
        return (self.x, self.y)
    
    @property
    def left(self):
        return self.x

    @property
    def rect(self):
        return self._rect

    @property
    def width(self):
        return self.image.get_width()

    @property
    def height(self):
        return self.image.get_height()

    @property
    def size(self):
        return (self.width, self.height)

    def set_enabled(self, enabled = True):
        # print('{} - enabled: {}'.format(self.id, enabled))
        self._enabled = enabled

    # TODO: Remove get_size, get_width and get_height
    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()
    
    def set_callback(self, callback = None):
        '''
        omit parameter to set to None
        '''
        self._callback = callback
        
    def get_size(self):
        return (self.image.get_width(), self.image.get_height())

    def check_mousepos(self, pos):
        if self._enabled:
            return self._rect.collidepoint(pos)
        else:
            return False

    def update(self):
        pass

    def on_click(self):
        if self._enabled:
            if self._callback:
                self._callback(self.id)
            else:
                print ('clicked: [{}] - '.format(self.id))
    


    def draw(self, surface):
        if self._enabled:
            surface.blit(self.image, (self.x, self.y))


# class Layout:
#     '''
#     Default -> this is also Flow_Layout - puts components in a single row
#     '''
#     def __init__(self, align = 'left', padding = (0,0)):
#         '''
#         align can be left, right, center
#         padding is (horizontal, vertical)
#         '''
#         self.align = align
#         self.padding = padding

#         self.controls = []

#     def _get_next_postion(self):
#         pass

#     def add_control(self, control):

#         self.controls.append(control)



# class Box_Layout(Layout):
#     ''' 
#     Like (Flow_)Layout, but puts components in a single column
#     '''
#     pass

# class Card_Layout(Layout):
#     '''
#     Create a 'tabbed' style layout, basically multiple layouts unioned
#     '''
#     pass

# class Grid_Layout(Layout):
#     '''
#     Creates a Grid style layout
#     '''
#     pass


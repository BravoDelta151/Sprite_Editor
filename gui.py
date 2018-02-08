import os
import pygame
from pygame.locals import *
from helpers import *
from sprite import *
from tile_editor import *
from strip_map import *
from components import *

class GUI:

    def __init__(self):
        pygame.init()

        self.x, self.y = 10, 10
        self.width, self.height = 1000, 600

        self.FPS = 30
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 16)      
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        
        self._set_display_name("untitled")

        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((40, 190,120))

        self.background_layers = []
        self.background_layers.append(background)

        self.screen.blit(background, (0, 0))
        self.sprites = []
                
        self.palette = Palette.init_from_file(get_dir_path("data", "palette_nes_decimal.txt"))
        self.show_palette = True

        self.tile_editor = Tile_Editor(self, 10,10, 512, 512, self.palette)
        self.strip_map = Strip_Map(self.width - 390 , 10,get_dir_path("images", "16x256.bmp"))
        
        self.anim_panel = Anim_Panel(self, self.width - 310, self.y + 100, 300, 330, size = 128 )

        self.running = True

    def _set_display_name(self, text):
        if text == "16x256":
            self._display_name = "untitled"
        else:
            self._display_name = text

        pygame.display.set_caption("Sprite Editor  --  {}".format(self._display_name))

    def handle_events(self):
        ''' Handles top level events and calls sub components 
        '''    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                # self.running = False
                self.handle_keypress(event)
                return
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mousemove(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mousebutton(event)
            else:
                pass

    def track_changes(self):
        # TODO: for undo/redo operation.  
        # Implement on tile_editor (sub pixels)
        pass

    def update(self):
        pass

    def draw(self):
        ''' 
        Top level function to draw all images
            calls subcomponents draw functions
        '''
        for bg in self.background_layers:
            self.screen.blit(bg, (0,0))

        if self.sprites and len(self.sprites) > 0:
            for sp in self.sprites:
                sp.draw(self.screen)

        if self.show_palette:
            self.palette.draw(self.screen, (self.width - 300 ,10))

        self.tile_editor.draw(self.screen)

        if self.strip_map:
            self.strip_map.draw(self.screen)
        
        self.anim_panel.draw(self.screen)

        pygame.display.flip()

    def _msg_box_prompt(self, label):
        '''
        Base message box call
        '''
        size = (250, 50)
        posx = (self.width/2 - size[0]/2) - self.x
        posy = self.y + 50 # (self.height/4 - size[1]/2) - self.y
        prompt = Prompt(self.screen, (posx,posy), size, label)
        prompt.text_boxes.append(Text_Box((posx+55, posy+20), (160, 18), 'Name', 'all'))

        return prompt.run(self.screen)

    def _save_bank(self, file_name, overwrite = False):
        '''
        '''
        restricted_list = ["", "untitled", "16x256"]

        if file_name in restricted_list:
            name = self.save_prompt()
        else:
            name = file_name

        if name not in restricted_list:
            name_bmp = "{}.bmp".format(name)
            file_list = get_file_list('banks')
            if name_bmp in file_list and overwrite == False:
                # TODO: Prompt message box with error messsage
                print("SAVE: --- Invalid File Name")
            else:
                full_name = get_dir_path("banks", name_bmp)
                pygame.image.save(self.strip_map.image, full_name)
                print("Saved: {}".format(full_name))

    def save_prompt(self):
        '''
        Display message box to bank 
        '''
        file_name = self._msg_box_prompt('Save Bank As')
        self._save_bank(file_name)

    def _load_bank(self, file_name):
        '''
        Loads a bank.  Moved out of load_prompt to handle
        New button which simply loads a blank strip
        '''
        if file_name:
            full_filename = get_dir_path("banks", file_name + ".bmp")
            check = os.path.isfile(full_filename)
            if check:   
                if self.strip_map:
                    self.strip_map.load_strip(full_filename)
                    self.tile_editor.set_image(self.strip_map.get_frame(0))
                    self.anim_panel.reset()
                else:
                    self.strip_map = Strip_Map(self.width - 390 , 10, full_filename)
                self._set_display_name(file_name)
            else:
                print("Invalid file name")


    def load_prompt(self,shift_key = True):
        '''
        Display message box to load a bank
        '''
        # file_list = get_file_list('images')
        file_name = self._msg_box_prompt('Load Bank') 
        self._load_bank(file_name)        
            

    def handle_keypress(self, evt):

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_q]:
            self.running = False        
        
        if pressed_keys[pygame.K_o]:
            # pressing 'o' prompts to enter filename
            # shift - o reads image directory and lists in terminal 
            self.load_prompt(pressed_keys[pygame.K_LSHIFT])                  

        if pressed_keys[pygame.K_p]:
            self.show_palette = not self.show_palette

        if pressed_keys[pygame.K_s] and pressed_keys[pygame.K_LCTRL]:
            self.save_prompt()

        if pressed_keys[pygame.K_n] and pressed_keys[pygame.K_LCTRL]:
            pass # TODO: New

    def handle_mousemove(self, event):
        x, y = event.pos
        # print("{} <> {}".format(self.tile_editor.right, x))
        if self.tile_editor.right > x:
            # print("{} > {}".format(self.tile_editor.right, x))
            pygame.mouse.set_cursor(*(self.tile_editor.cursor))
        else:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)

    def handle_mousebutton(self, event):
        # print(event)
        self.tile_editor.handle_click(event.pos, event.button)
        
        if self.show_palette:
            self.palette.handle_click(event.pos, event.button)
        
        if self.strip_map:
            if self.strip_map.check_click(event.pos):
                frame, changed = self.strip_map.handle_click(event.pos)
                # print (changed)
                if frame and event.button == 3:
                    self.anim_panel.add_cell(frame)
                elif changed and frame:
                    self.tile_editor.set_image(frame)

        self.anim_panel.handle_click(event.pos, event.button)


    def run(self):
        '''
        main loop 
        '''
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)
        
        pygame.quit()


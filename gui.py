import os
import pygame
from pygame.locals import *
from helpers import *
from sprite import *
from tile import *
from strip_map import *
from message_box import *



class GUI:

    def __init__(self):
        pygame.init()

        self.x, self.y = 10, 10
        self.width, self.height = 1000, 600

        self.FPS = 30
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 16)      
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Sprite Editor")

        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((40, 190,120)) # 0, 15, 40))

        self.background_layers = []
        self.background_layers.append(background)

        self.screen.blit(background, (0, 0))
        self.sprites = []
                
        self.palette = Palette.init_from_file(get_dir_path("data", "palette_nes_decimal.txt"))
        self.show_palette = True

        # set_cursor_from_image(self.cwd+'\\paintbrush_cursor_1.png', (4, 21))
        self.tile_editor = Tile_Editor(self, 10,10, 512, 512, self.palette)
        self.strip_map = Strip_Map(self.width - 390 , 10,get_dir_path("images", "16x256.bmp"))
        
        self.anim_panel = Anim_Panel(self, self.width - 310, self.y + 100, 300, 330, size = 256 )

        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                # self.running = False
                self.handle_keypress(event)
                return
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
        size = (250, 50)
        posx = (self.width/2 - size[0]/2) - self.x
        posy = self.y + 50 # (self.height/4 - size[1]/2) - self.y
        prompt = Prompt(self.screen, (posx,posy), size, label)
        prompt.text_boxes.append(Text_Box((posx+55, posy+20), (160, 18), 'Name', 'all'))

        return prompt.run(self.screen)

    def save_prompt(self):
        name = self._msg_box_prompt('Save Bank As')        
        if name:
            print(name)
        #     if name.lower() == 'pymap':
        #         self.post_status('SAVE FAILED: \'pyMap\' is a reserved map name')
        #         return
        #     if os.path.isdir(cwd+'\\Maps\\'+name):
        #         self.post_status('SAVE FAILED: The name provided is already in use by another map')
        #         surface.fill((0,0,0))
        #         self.draw(surface)
        #         pygame.display.flip()
        #         self.save_as_prompt(surface)
        #     else:
        #         self.name = name
        #         os.mkdir(cwd+'\\Maps\\'+name)
        #         self.save()

    def load_prompt(self,shift_key = True):
        '''
        TODO: Implement message box prompt
        '''
        # file_list = get_file_list('images')
        file_name = self._msg_box_prompt('Load Bank') 
        if file_name:
            # print(file_name)

            full_filename = get_dir_path("banks", file_name + ".bmp")
            # print(full_filename)
            check = os.path.isfile(full_filename)
            if check:   
                if self.strip_map:
                    self.strip_map.load_strip(full_filename)
                    self.tile_editor.set_image(self.strip_map.get_frame(0))
                else:
                    self.strip_map = Strip_Map(self.width - 390 , 10, full_filename)
            else:
                print("Invalid file name")

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


    def handle_mousebutton(self, event):
        # print(event)
        self.tile_editor.handle_click(event.pos, event.button)
        
        if self.show_palette:
            self.palette.handle_click(event.pos, event.button)
        
        if self.strip_map:
            if self.strip_map.check_click(event.pos):
                frame, changed = self.strip_map.handle_click(event.pos)
                print (changed)
                if changed and frame:
                    self.tile_editor.set_image(frame)
                    
        self.anim_panel.handle_click(event.pos, event.button)


    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)
        
        pygame.quit()


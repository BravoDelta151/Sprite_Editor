import os
import pygame
from pygame.locals import *
from sprite import *
from tile import *
from strip_map import *
from message_box import *

def get_file_list(dir):
    files = []
    cwd = os.getcwd()
    path = '{}\\{}'.format(cwd, dir)
    # print("Checking {}".format(path))
    lst = os.listdir(path)
    for f in lst:
        # print(f)
        if not f.startswith('.'):
            files.append(f)

    return files

class GUI:

    def __init__(self):
        pygame.init()

        self.x = 10
        self.y = 10

        self.width = 1000
        self.height = 700

        self.FPS = 30
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 16)
        self.cwd = os.getcwd()

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Sprite Viewer")

        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((40, 190,120)) # 0, 15, 40))

        self.background_layers = []
        self.background_layers.append(background)

        self.screen.blit(background, (0, 0))
        self.sprites = []
        
        data_dir = os.path.join(self.cwd, 'data')
        self.palette = Palette.init_from_file(os.path.join(data_dir, 'palette_nes_decimal.txt'))
        self.show_palette = True

        # set_cursor_from_image(self.cwd+'\\paintbrush_cursor_1.png', (4, 21))
        self.tile_editor = Tile_Editor(10,10, 512, 512, self.palette)

        self.strip_map = None
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
            
    def update(self):
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

        pygame.display.flip()


    def load_file(self,shift_key = True):
        '''
        TODO: Implement message box prompt
        '''
        prompt = "Enter filename: "
        file_list = None
        file_name = "16x256.bmp" 

        if shift_key:
            file_list = get_file_list('images')
            
            if len(file_list) > 0:
                prompt = "Select file number: "
                for idx, f in enumerate(file_list):
                    print('{} - {}'.format(idx, f))
            
        x = input(prompt)

        # print('x: {}, nx: {}'.format(x, nx))
        if x.isdigit and file_list:
            nx = int(x)
            if nx >= 0 and nx < len(file_list):
                print("Selected: {}".format(file_list[nx]))
                file_name = file_list[nx]
            else:
                print("Invalid selection")
        else:
            file_name = x

        full_filename = '{}\\images\\{}'.format(self.cwd, file_name)
        check = os.path.isfile(full_filename)
        if check:            
           self.strip_map = Strip_Map(self.width - 300 , 90, full_filename)
        else:
            print("Invalid file name")



    def handle_keypress(self, evt):

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_q]:
            self.running = False        
        
        if pressed_keys[pygame.K_o]:
            # pressing 'o' prompts to enter filename
            # shift - o reads image directory and lists in terminal 
            self.load_file(pressed_keys[K_LSHIFT])                  

        if pressed_keys[pygame.K_p]:
            self.show_palette = not self.show_palette


    def handle_mousebutton(self, event):
        # print(event)
        self.tile_editor.handle_click(event.pos, event.button)
        
        if self.show_palette:
            self.palette.handle_click(event.pos, event.button)
        
        if self.strip_map:
            if self.strip_map.check_click(event.pos):
                frame = self.strip_map.handle_click(event.pos)
                if frame:
                    self.tile_editor.set_image(frame)
                

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.clock.tick(self.FPS)
        
        pygame.quit()


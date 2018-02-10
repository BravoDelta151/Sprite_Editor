# Helper functions 
import pygame
import os

def set_cursor_from_image(image, hotspot = (0,0)):
    #if os.path.isfile((cwd+'/'+image)):
    w,h = image.get_size()
    strings = []
    size = (w,h)
    if w%8 == 0 and h%8 == 0:
        black = pygame.Color(0,0,0,255)
        white = pygame.Color(255,255,255,255)
        trans = pygame.Color(255,0,255,255)
        image.lock()
        for r in range(0, w):
            pix_str = ""
            for c in range(0, h):
                color = image.get_at((r,c))
                if color == white:
                    pix_str += 'X'
                if color == black:
                    pix_str += '.'
                if color == trans:
                    pix_str += ' '
            strings.append(pix_str)
        image.unlock()
        new_cursor = pygame.cursors.compile(strings)
        pygame.mouse.set_cursor(size, hotspot, *new_cursor)

def get_text_rendered(text, color = (0,0,0), font_name = None, font_size = 14):
    font = pygame.font.Font(font_name, font_size)
    return font.render(text, True, color)

def get_dir_path(dirname = "", filename=None):
    cwd = os.getcwd()
    data_dir = os.path.join(cwd, 'data')
    image_dir = os.path.join(cwd, 'images')
    bank_dir = os.path.join(cwd, "banks")

    if dirname and dirname.lower() == "data":
        if filename:
            return os.path.join(data_dir, filename)
        else:
            return data_dir
    elif dirname and dirname.lower() == "images":
        if filename:
            return os.path.join(image_dir, filename)
        else:
            return image_dir
    elif dirname and dirname.lower() == "banks":
        if filename:
            return os.path.join(bank_dir, filename)
        else:
            return bank_dir
    else:
        return cwd


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

def load_file(filename):
    image = None
    try:
        image = pygame.image.load(filename).convert()
    except pygame.error:
        print ("Unable to load spritesheet image: {}".format(filename))    
        raise SystemExit(pygame.get_error())

    return image
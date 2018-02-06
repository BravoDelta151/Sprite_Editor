# Helper functions 
import pygame
import os

def get_dir_path(dirname = "", filename=None):
    cwd = os.getcwd()
    data_dir = os.path.join(cwd, 'data')
    image_dir = os.path.join(cwd, 'images')

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
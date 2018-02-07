#https://www.pygame.org/wiki/Spritesheet
# # This class handles sprite sheets
# This was taken from www.scriptefun.com/transcript-2-using
# sprite-sheets-and-drawing-the-background
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)

import pygame

class spritesheet(object):

    def __init__(self, image):
         self.sheet = image

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip_vertical(self, rect, image_count, colorkey = None):
        tups = [(rect[0], rect[1] + rect[3] * y, rect[2], rect[3])
                for y in range(image_count)]
        return self.images_at(tups, colorkey)

    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)


class SpriteStripAnim(object):
    """sprite strip animator
    
    This class provides an iterator (iter() and next() methods), and a
    __add__() method for joining strips which comes in handy when a
    strip wraps to the next row.
    """
    def __init__(self, image, rect, count, colorkey=None, loop=False, frames=1):
        """construct a SpriteStripAnim
        
        filename, rect, count, and colorkey are the same arguments used
        by spritesheet.load_strip.
        
        loop is a boolean that, when True, causes the next() method to
        loop. If False, the terminal case raises StopIteration.
        
        frames is the number of ticks to return the same image before
        the iterator advances to the next image.
        """
        self.cell_rect = pygame.Rect(rect)
        if image and count > 0:
            ss = spritesheet(image)
            self.cells = ss.load_strip_vertical(rect, count, colorkey)
        else:
            self.cells = []
        

        self.current_frame = 0
        self.loop = loop
        self.frames = frames
        self.skip_frame = frames
        self.start_frame = 0
        self.end_frame = len(self.cells) - 1

    @property
    def count(self):
        return len(self.cells)

    def set_start_frame(self, index = 0):
        self.start_frame = index

    def set_end_frame(self, index = -1):
        if index < 0:
            self.end_frame = self.count - 1
        elif index < self.count:
            self.end_frame = index


    def flip(self, xbool = False, ybool = False):
        for i in range(len(self.cells)):
            self.cells[i] = pygame.transform.flip(self.cells[i], xbool, ybool)

    def scale(self, scale):
        for i in range(len(self.cells)):
            if scale == 2:
                self.cells[i] = pygame.transform.scale2x(self.cells[i])
            else:
                w, h = self.cells[i].get_size()
                self.cells[i] = pygame.transform.scale(self.cells[i], (w * scale, h * scale))

    def rotate(self, angle):
        for i in range(len(self.cells)):
            self.cells[i] = pygame.transform.rotate(self.cells[i], angle)

    def inc_frame_rate(self):
        self.set_frame_rate(self.frames + 1)

    def dec_frame_rate(self):
        self.set_frame_rate(max(1, self.frames - 1))

    def set_frame_rate(self, frame_rate):
        # print("Setting frames to {}".format(frames))
        self.frames = frame_rate
        self.skip_frame = 0
        # self.i = 0

    def iter(self):
        self.current_frame = 0
        self.skip_frame = self.frames
        return self

    def next(self):
        if self.count <= 0:
            return False

        if self.current_frame >= len(self.cells):
            if not self.loop:
                raise StopIteration
            else:
                self.current_frame = 0
        image = self.cells[self.current_frame]
        self.skip_frame -= 1
        if self.skip_frame <= 0:
            self.current_frame += 1
            self.skip_frame = self.frames
        return image

    def append(self, image):
        self.cells.append(image)

    def __add__(self, ss):
        self.cells.extend(ss.cells)
        return self

    def update_cell(self, image, index):
        if index < -1 or index >= self.count:
            print("SpriteStrip: Invalid Index: {}".format(index))
        elif image.get_size() != self.cell_rect.size:
            print("SpriteStrip: update_cell - size mismatch {} != {}".format(image.get_size(), self.cell_rect.size))
        else:
            # cells = []
            # for i in range(self.count):
            #     if i == index:
            #         cells.append(image)
            #     else:
            #         cells.append(self.cells[i])
            # self.cells.clear()
            # self.cells = cells
            for x in range(image.get_width()):
                for y in range(image.get_height()):
                    color = image.get_at((x,y))
                    self.cells[index].set_at((x,y), color)
            

    def add_cell(self, image):
        if image.get_size() == self.cell_rect.size:
            self.cells.append(image)
        else:
            iw, ih = image.get_size()
            print("Invalid image {}, {} != {}, {}".format(iw, ih, self.cell_rect.width, self.cell_rect.height) )

    def delete_cell(self, index = -1):
        '''
        omitting index will clear entire list
        '''
        if index < 0:
            self.cells.clear()
        elif index < self.count:
            del self.cells[index]
        

    def get_frame(self, frame_index = 0):
        frame = None
        if frame_index < -1 or frame_index >= len(self.cells):
            print('Invalid frame index [{}]'.format(frame_index))
        else:
            # print ("getting frame {}".format(frame_index))
            frame = self.cells[frame_index]
        return frame

        

class Sprite:
    def __init__(self, image, x, y, width, height, count, frame_rate = 1, loop = True):
        self.image = image
        self.x = x
        self.y = y
        self.z = 0

        self.rect = pygame.Rect(0, 0, width, height)

        self.velocity_x = 0
        self.velocity_y = 0

        self.dir_x = 0
        self.dir_y = 0

        self.strip = SpriteStripAnim(self.image, (0,0,width,height), count, colorkey = (255,0,255), loop = loop, frames = frame_rate )
        self._animate = False

    def scale(self, scale):
        '''
        Scale all cells in a sprite strip
        '''
        self.strip.scale(scale)

    def flip(self, vert = False, horiz = False):
        '''
        Flip all cell images vertically and/or horizontally
        '''
        self.strip.flip(vert, horiz)

    def rotate(self, angle):
        '''
        rotate all cell images by angle, 
        '''
        self.strip.rotate(angle)

    def move_to(self, x, y):
        '''
        Move sprite to location
        '''
        self.x = x
        self.y = y

    def animate(self, stop = False):
        self._animate = not stop

    def draw(self, surface):
        '''
        Draw sprite on supplied surface
        '''
        if self._animate:
            image = self.strip.next()

        if image:
            surface.blit(image, (self.x, self.y)) #  (self.width // 2 - w // 2, self.height // 2 - h // 2))


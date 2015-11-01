from PIL import Image, ImageDraw
from threading import Thread
import math

class Stick(Thread):
    def __init__(self, image, depth, max_depth, x, y, angle, length, width,
                 left_branch_length, right_branch_length, left_branch_resize, right_branch_resize,
                 left_branch_width, right_branch_width, left_branch_width_loss, right_branch_width_loss,
                 angle_between_branches):
        super(Stick, self).__init__()
        self.image = image
        self.max_depth = max_depth
        self.depth = depth
        self.x = x
        self.y = y
        self.angle = angle
        self.length = length
        self.width = width
        self.left_branch_length = left_branch_length
        self.right_branch_length = right_branch_length
        self.left_branch_resize = left_branch_resize
        self.right_branch_resize = right_branch_resize
        self.left_branch_width = left_branch_width
        self.right_branch_width = right_branch_width
        self.left_branch_width_loss = left_branch_width_loss
        self.right_branch_width_loss = right_branch_width_loss
        self.angle_between_branches = angle_between_branches
        self.rad = math.pi / 180

    def run(self):

        next_x = self.x + math.cos(self.angle * self.rad) * self.length
        next_y = self.y + math.sin(self.angle * self.rad) * self.length
        self.image.line((self.x, self.y, next_x, next_y), fill=0, width=self.width)
        if ++self.depth is not self.max_depth:
            angle = self.angle_between_branches / 2
            left_stick = Stick(self.image, self.depth + 1, self.max_depth, next_x, next_y,
                               self.angle - angle, self.left_branch_length, self.left_branch_width,
                               self.left_branch_length * self.left_branch_resize,
                               self.right_branch_length * self.right_branch_resize,
                               self.left_branch_resize, self.right_branch_resize,
                               self.left_branch_width - self.left_branch_width_loss,
                               self.right_branch_width - self.right_branch_width_loss,
                               self.left_branch_width_loss, self.right_branch_width_loss,
                               self.angle_between_branches)


            rigth_stick = Stick(self.image, self.depth + 1, self.max_depth, next_x, next_y,
                                self.angle + angle, self.right_branch_length, self.right_branch_width,
                                self.left_branch_length * self.left_branch_resize,
                                self.right_branch_length * self.right_branch_resize,
                                self.left_branch_resize, self.right_branch_resize,
                                self.left_branch_width - self.left_branch_width_loss,
                                self.right_branch_width - self.right_branch_width_loss,
                                self.left_branch_width_loss, self.right_branch_width_loss,
                                self.angle_between_branches)
            left_stick.start()
            left_stick.join()
            rigth_stick.start()
            rigth_stick.join()

im = Image.new('RGB', (2000, 2000), (255, 255, 255, 255))
draw = ImageDraw.Draw(im)
s = Stick(draw,         #image
          0,            #current depth
          12,           #max depth
          1000,         #position x
          2000,         #position y
          270,          #angle
          100,          #length
          10,           #width
          200,          #left branch length
          200,          #right branch length
          0,          #left branch resize
          0.9,          #right branch resize
          10,           #left branch width
          10,           #right branch width
          1,            #left branch width loss
          1,           #right branch width loss
          45)           #angle between branches
s.start()
s.join()

im.show()
im.save("abcd.ppm", "ppm")
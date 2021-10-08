import tkinter
import random

TIME = 20  # Whole time in seconds
FPS = 60  # Frames per second
N = 5  # Number of targets
WIDTH = 500  # Window width in pixels
HEIGHT = 500  # Window height in pixels
V_MAX = 100  # Max velocity on one axis in pixels per second
RADIUS = 20  # Target radius in pixels
TYPES = ['Polygon', 'Ball']  # Types available for creating

filename = 'leaderboard.txt'  # Leaderboard filename


class Target:
    def __init__(self, canvas, tar_type, color, x, y, vx, vy, radius):
        """
        Creates Target Class object
        :param canvas: Tk.Canvas object where target should be painted
        :param tar_type: type of target. Must be 'Ball' or 'Polygon'
        :param color: target color in rgb hex format, for ex. '#ff0000' is red
        :param x: x center coordinate in pixels
        :param y: y center coordinate in pixels
        :param vx: velocity on axis x in pixels per second
        :param vy: velocity on axis y in pixels per second
        :param radius: radius in pixels.
        """
        self.alive = True
        self.canvas = canvas
        self.tar_type = tar_type.lower()
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        if self.tar_type == 'ball':
            self.painting = self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                                    fill=color, outline='')
        elif self.tar_type == 'polygon':
            self.painting = self.canvas.create_polygon((x - radius, y - radius), (x + radius, y - radius),
                                                       (x, y + radius), fill=color, outline='')
        else:
            raise Exception('Incorrect target type')
        self.canvas.tag_bind(self.painting, '<Button-1>', self.on_click)

    def update(self, dt):
        """
        Updates coordinates after dt time and moves painting on canvas to actual coordinates.
        Also checks collisions with canvas borders.
        :param dt: time after last update in seconds
        """
        delta_x = dt * self.vx
        delta_y = dt * self.vy
        self.x += delta_x
        self.y += delta_y
        if self.x < self.radius or self.x > self.canvas.winfo_width() - self.radius:
            self.vx = - self.vx
            if self.tar_type == 'polygon':
                self.vy = self.vy * random.random() * 2
        if self.y < self.radius or self.y > self.canvas.winfo_height() - self.radius:
            self.vy = - self.vy
            if self.tar_type == 'polygon':
                self.vx = self.vx * random.random() * 2

        self.canvas.move(self.painting, delta_x, delta_y)

    def on_click(self, event=None):
        """
        Function that add some points to score depending on target type and delete painting on canvas.
        """
        global score
        if self.tar_type == 'ball':  # Adds 1 to score if ball
            score += 1
        elif self.tar_type == 'polygon':  # Adds 2 to score if polygon
            score += 2
        else:
            score += 1
            print('Unexpected target type')

        self.canvas.delete(self.painting)
        self.alive = False
        #print(score)


def main_cycle(time_left):
    """
    Main cycle of program. Updates all targets and creates new one if necessary.
    Calls itself after 1000 // FPS delay.
    :param time_left: time remaining until the end of work in seconds
    """
    for tar in targets:
        if tar.alive:
            tar.update(1 / FPS)
        else:
            targets.remove(tar)

    if len(targets) < N:
        targets.append(Target(canvas, random.choice(TYPES), "#{:06x}".format(random.randint(0, 0xFFFFFF)),
                              random.randint(RADIUS, WIDTH - RADIUS), random.randint(RADIUS, HEIGHT - RADIUS),
                              random.randint(0, V_MAX), random.randint(0, V_MAX), RADIUS))

    if time_left > 0:
        time_left -= 1 / FPS
        root.after(1000 // FPS, lambda: main_cycle(time_left))
    else:
        end_work()


def end_work():
    """
    Destroys window and writes scoreline in leaderboard file
    """
    root.destroy()
    name = input('Enter your name: ')
    file = open(filename, 'a')
    file.write(name + ' got ' + str(score) + ' score in ' + str(TIME) + ' seconds\n')
    file.close()
    print(name, score)


score = 0
root = tkinter.Tk()
canvas = tkinter.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

targets = []
main_cycle(TIME)

root.mainloop()

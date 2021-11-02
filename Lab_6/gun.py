import random
import tkinter
import math


FPS = 144
WIDTH = 1000
HEIGHT = 500
G = 0.5
TIME_ACCELERATION = 15
POWER = 7


class GameMaster:
    def __init__(self, fps, width, height, g, time_acceleration, power):
        """
        Starts new game
        :param fps: frames per second
        :param width: window width in pixels
        :param height: window height in pixels
        :param g: acceleration of gravity
        :param time_acceleration: time acceleration
        :param power: gun power
        """
        self.fps = fps
        self.width = width
        self.height = height
        self.g = g
        self.time_acceleration = time_acceleration
        self.power = power

        self.result_text = None
        self.shells_text = None
        self.shells = []
        self.targets = []
        self.guns = []

        self.root = tkinter.Tk()
        self.root.title('Gun')
        self.canvas = tkinter.Canvas(self.root, height=self.height, width=self.width)
        self.canvas.pack(fill=tkinter.BOTH, expand=1)

        self.start_game()
        self.root.mainloop()

    def main_cycle(self):
        """
        Main cycle. Updates all shells and guns. Checks collisions with targets.
        Calls itself after (1000 // FPS) ms delay if there are targets alive.
        """
        dt = self.time_acceleration / self.fps
        alive = False

        self.canvas.itemconfig(self.shells_text, text=len(self.shells))
        for gun in self.guns:
            gun.power_up(dt)
            if len(gun.create_shell):
                self.shells.append(Shell(self.canvas, *gun.create_shell))
                gun.create_shell = []

        for target in self.targets:
            for ball in self.shells:
                ball.move(dt, self.g)
                if ball.hit_test(target) and target.alive:
                    target.alive = False
                    self.canvas.delete(target.painting)
                    self.result_text = self.canvas.create_text(self.width / 2, self.height / 2,
                                                               text='You destroyed targets in ' +
                                                                    str(len(self.shells)) +
                                                                    ' shots')
            if target.alive:
                alive = True

        if alive:
            self.root.after(1000 // self.fps, self.main_cycle)
        else:
            self.root.after(5000, self.end_game)

    def start_game(self):
        """
        Starts new round. Creates guns and targets and calls main cycle
        """
        self.shells_text = self.canvas.create_text(30, 30, text=len(self.shells))
        self.shells = []
        self.targets = [Ball(self.canvas, '#000000', random.randint(20, self.width - 20),
                             random.randint(20, self.height - 20),  20)]
        self.guns = [Gun(self.canvas, '#000000', 10, self.height - 10, self.power)]

        self.main_cycle()

    def end_game(self):
        """
        Ends round. Destroys every entity in canvas and calls function that starts new round.
        """
        self.canvas.delete(self.result_text)
        self.canvas.delete(self.shells_text)
        for obj in self.shells + self.guns:
            self.canvas.delete(obj.painting)

        self.start_game()


class Ball:
    def __init__(self, canvas, color, x, y, radius):
        """
        Creates Ball on Canvas.
        :param canvas: Canvas object
        :param color: ball's color in rgb hex, for ex. '#ff0000' is red
        :param x: x coordinate of center in pixels
        :param y: y coordinate of center in pixels
        :param radius: radius in pixels
        """
        self.canvas = canvas
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.alive = True
        self.painting = self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                                fill=color)


class Shell(Ball):
    def __init__(self, canvas, color, x, y, radius, vx, vy):
        """
        Creates Shell object.
        :param canvas: Canvas object
        :param color: shell's color in rgb hex, for ex. '#ff0000' is red
        :param x: x coordinate of center in pixels
        :param y: y coordinate of center in pixels
        :param radius: radius in pixels
        :param vx: velocity on axis x in pixels per second
        :param vy: velocity on axis y in pixels per second
        """
        super().__init__(canvas, color, x, y, radius)
        self.vx = vx
        self.vy = vy

    def move(self, dt, g):
        """
        Updates coordinates after dt time and moves painting on canvas
        to actual coordinates.
        Also checks collisions with canvas borders.
        :param dt: time after last update in seconds
        :param g: acceleration of gravity
        """
        delta_x = dt * self.vx
        delta_y = dt * self.vy + g * dt**2 / 2
        self.x += delta_x
        self.y += delta_y

        self.vy += dt * g

        if self.x < self.radius or self.x > self.canvas.winfo_width() - self.radius:
            self.vx = - self.vx
        if self.y < self.radius or self.y > self.canvas.winfo_height() - self.radius:
            self.vy = - self.vy

        self.canvas.move(self.painting, delta_x, delta_y)

    def hit_test(self, obj):
        """
        Function that checks collision between current object and object given in argument.
        :param obj: object to check for collision
        :return: True if there is a collision and False if there is no
        """
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 < (self.radius + obj.radius)**2:
            return True
        else:
            return False


class Gun:
    def __init__(self, canvas, color, x, y, power, length=20, width=10):
        """
        Creates Gun object.
        :param canvas: tkinter Canvas object
        :param color: gun's color in rgb hex, for ex. '#ff0000' is red
        :param x: x coordinate of center in pixels
        :param y: y coordinate of center in pixels
        :param power: projectile velocity coefficient from this gun
        :param length: gun's length in pixels
        :param width: gun's width in pixels
        """
        self.canvas = canvas
        self.color = color
        self.x = x
        self.y = y
        self.power = power
        self.length = length
        self.width = width

        self.charged = 1
        self.charging = False
        self.create_shell = []
        self.angle = 0
        self.painting = self.canvas.create_line(self.x, self.y, self.x + self.length, self.y,
                                                width=self.width, fill=self.color)

        self.canvas.bind('<Button-1>', self.charging_start)
        self.canvas.bind('<ButtonRelease-1>', self.charging_end)
        self.canvas.bind('<Motion>', self.targeting)

    def charging_start(self, event=None):
        """
        Changes gun's state to charging.
        :param event: tkinter Event object
        """
        self.charging = True

    def charging_end(self, event):
        """
        Saves the state of the gun for the subsequent creation of a shell and
        resets charging state of the gun.
        :param event: tkinter Event object
        """
        self.angle = math.atan((event.y - self.y) / (event.x - self.x))
        vx = self.charged * self.power * math.cos(self.angle)
        vy = self.charged * self.power * math.sin(self.angle)

        self.create_shell = ['#FF0000', self.x, self.y, 5, vx, vy]
        self.charging = False
        self.charged = 1
        self.targeting()

    def targeting(self, event=None):
        """
        Updates painting on Canvas so the gun looks directly at the mouse.
        :param event: tkinter Event object
        """
        if event and event.x != self.x:
            self.angle = math.atan((event.y - self.y) / (event.x - self.x))

        self.canvas.coords(self.painting, self.x, self.y,
                           self.x + (math.cos(self.angle) * self.length * self.charged),
                           self.y + (math.sin(self.angle) * self.length * self.charged))

    def power_up(self, dt):
        """
        Increases gun's charging power and updates painting on Canvas.
        :param dt: dt in seconds after last update
        """
        if self.charging:
            if self.charged < 5:
                self.charged += dt
                self.canvas.coords(self.painting, self.x, self.y,
                                   self.x + (math.cos(self.angle) * self.length * self.charged),
                                   self.y + (math.sin(self.angle) * self.length * self.charged))
            self.canvas.itemconfig(self.painting, fill='#FF7F00')
        else:
            self.canvas.itemconfig(self.painting, fill=self.color)


GameMaster(FPS, WIDTH, HEIGHT, G, TIME_ACCELERATION, POWER)

# TODO Улучшите программу из №1 добавив 2 цели.
# TODO Улучшите программу из №2 сделав цели движущимися.
# TODO Сделать несколько типов снарядов.
# TODO Реализоваль несколько типов целей с различным характером движения.
# TODO Сделать пушку двигающимся танком.
# TODO Создать "бомбочки", которые будут сбрасывать цели на пушку.
# TODO Сделать несколько пушек, которые могут стрелять друг в друга.

import random
import tkinter
import math
import json


FPS = 144
WIDTH = 1000
HEIGHT = 500
G = 0.5
TIME_ACCELERATION = 15
POWER = 7
V_MAX = 5
N = 3
TYPES = ['Triangle', 'Ball']  # Types available for creating
FILENAME = 'leaderboard.json'  # Leaderboard filename


class GameMaster:
    def __init__(self, fps, width, height, g, time_acceleration, power, v_max=0, n=1,
                 types=None, filename=None):
        """
        Starts new game
        :param fps: frames per second
        :param width: window width in pixels
        :param height: window height in pixels
        :param g: acceleration of gravity
        :param time_acceleration: time acceleration
        :param power: gun power
        :param v_max: max velocity on one axis in pixels per second
        :param n: number of targets
        """
        self.fps = fps
        self.width = width
        self.height = height
        self.g = g
        self.time_acceleration = time_acceleration
        self.power = power
        self.v_max = v_max
        self.n = n
        self.types = types
        self.filename = filename

        self.name_entry = None
        self.name_label = None
        self.result_text = None
        self.shells_text = None
        self.score = None
        self.shells = []
        self.targets = []
        self.guns = []
        self.bombs = []

        self.root = tkinter.Tk()
        self.root.title('Gun')
        self.canvas = tkinter.Canvas(self.root, height=self.height, width=self.width)
        self.canvas.pack(fill=tkinter.BOTH, expand=1)

        self.save_button = tkinter.Button(self.root, command=self.end_session, text='End Game')
        self.save_button.pack()

        self.start_game()
        self.root.mainloop()

    def main_cycle(self):
        """
        Main cycle. Updates all shells and guns. Checks collisions with targets.
        Calls itself after (1000 // FPS) ms delay if there are targets alive.
        """
        dt = self.time_acceleration / self.fps
        alive = False

        self.canvas.itemconfig(self.shells_text, text=str(len(self.shells)) + ' (' +
                               str(self.score) + ')')
        for gun in self.guns:
            gun.power_up(dt)
            if len(gun.create_shell):
                self.shells.append(Shell(self.canvas, *gun.create_shell, self.g))
                gun.create_shell = []

                for target in self.targets:
                    if target.alive:
                        self.bombs.append(Bomb(self.canvas, 'Brown', target.x, target.y, 30, self.g))

        for target in self.targets:
            target.move(dt)
        for shell in self.shells:
            shell.move(dt)
        for bomb in self.bombs:
            bomb.move(dt)

        for target in self.targets:
            for shell in self.shells:
                if shell.hit_test(target) and target.alive:
                    target.alive = False
                    self.canvas.delete(target.painting)
            if target.alive:
                alive = True

        for bomb in self.bombs:
            if bomb.alive:
                for gun in self.guns:
                    if bomb.hit_test(gun):
                        self.end_game()
                        return

        if alive:
            self.root.after(1000 // self.fps, self.main_cycle)
        else:
            self.result_text = self.canvas.create_text(self.width / 2, self.height / 2,
                                                       text='You destroyed targets in ' +
                                                            str(len(self.shells)) + ' shots')
            if self.score:
                self.score = min(self.score, len(self.shells))
            else:
                self.score = len(self.shells)
            self.root.after(5000, self.end_game)

    def start_game(self):
        """
        Starts new round. Creates guns and targets and calls main cycle
        """
        self.shells_text = self.canvas.create_text(30, 30, text=str(len(self.shells)) + ' (' +
                                                   str(self.score) + ')')
        self.shells = []
        self.bombs = []
        self.targets = [MovingTarget(self.canvas, '#000000', random.randint(20, self.width - 20),
                                     random.randint(20, self.height - 20),  20,
                                     random.randint(0, self.v_max), random.randint(0, self.v_max))
                        for i in range(self.n)]
        self.guns = [Gun(self.canvas, '#000000', 10, self.height - 10, self.power)]
        self.root.bind('<Right>', self.guns[0].move_right)
        self.root.bind('<Left>', self.guns[0].move_left)

        self.main_cycle()

    def end_game(self):
        """
        Ends round. Destroys every entity in canvas and calls function that starts new round.
        """
        self.canvas.delete(self.result_text)
        self.canvas.delete(self.shells_text)
        for obj in self.shells + self.guns + self.targets + self.bombs:
            self.canvas.delete(obj.painting)

        self.start_game()

    def end_session(self):
        self.canvas.destroy()
        self.save_button.destroy()

        if self.score and self.filename:
            self.name_label = tkinter.Label(self.root, text='Enter your name:')
            self.name_label.pack()
            self.name_entry = tkinter.Entry(self.root)
            self.name_entry.pack()
            self.save_button = tkinter.Button(self.root, command=self.save_and_show, text='Save')
            self.save_button.pack()
            self.root.bind('<Return>', lambda event: self.save_and_show())
        else:
            self.root.destroy()

    def save_and_show(self):
        """
        Destroys objects, updates leaderboard json file and shows leaderboard table.
        """
        name = self.name_entry.get()
        self.name_entry.destroy()
        self.name_label.destroy()
        self.save_button.destroy()

        with open(self.filename, 'r') as f:
            loaded = json.load(f)
        loaded['results'].append({'name': name, 'points': self.score})
        with open(self.filename, 'w') as f:
            json.dump(loaded, f, indent=4)

        row = 0
        tkinter.Label(self.root, text='Leaderboard').grid(row=row, column=0, columnspan=2)

        for result in sorted(loaded['results'], key=lambda dic: dic['points']):
            row += 1
            tkinter.Label(self.root, text=result['name']).grid(row=row, column=0)
            tkinter.Label(self.root, text=result['points']).grid(row=row, column=1)


class Gun:
    def __init__(self, canvas, color, x, y, power):
        """
        Creates Gun object.
        :param canvas: tkinter Canvas object
        :param color: gun's color in rgb hex, for ex. '#ff0000' is red
        :param x: x coordinate of center in pixels
        :param y: y coordinate of center in pixels
        :param power: projectile velocity coefficient from this gun
        """
        self.canvas = canvas
        self.color = color
        self.x = x
        self.y = y
        self.power = power
        self.length = 20
        self.width = 10
        self.radius = self.length
        self.speed = 5

        self.charged = 1
        self.charging = False
        self.create_shell = []
        self.angle = 0
        self.painting = self.canvas.create_line(self.x, self.y, self.x + self.length, self.y,
                                                width=self.width, fill=self.color)

        self.canvas.bind('<Button-1>', self.charging_start)
        self.canvas.bind('<ButtonRelease-1>', self.charging_end)
        self.canvas.bind('<Motion>', self.targeting)

    def move_left(self, event=None):
        self.x -= self.speed
        if self.x > 0:
            self.canvas.coords(self.painting, self.x, self.y,
                               self.x + (math.cos(self.angle) * self.length * self.charged),
                               self.y + (math.sin(self.angle) * self.length * self.charged))
        else:
            self.x += self.speed

    def move_right(self, event=None):
        self.x += self.speed
        if self.x < self.canvas.winfo_width():
            self.canvas.coords(self.painting, self.x, self.y,
                               self.x + (math.cos(self.angle) * self.length * self.charged),
                               self.y + (math.sin(self.angle) * self.length * self.charged))
        else:
            self.x -= self.speed

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
        self.angle = -math.acos((event.x - self.x) /
                                ((event.x - self.x)**2 + (event.y - self.y)**2)**0.5)
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
        if event and not (event.x == self.x and event.y == self.y):
            self.angle = -math.acos((event.x - self.x) /
                                    ((event.x - self.x)**2 + (event.y - self.y)**2)**0.5)

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


class Ball:
    def __init__(self, canvas, color, x, y, radius, vx, vy):
        """
        Creates Ball on Canvas.
        :param canvas: Canvas object
        :param color: ball's color in rgb hex, for ex. '#ff0000' is red
        :param x: x coordinate of center in pixels
        :param y: y coordinate of center in pixels
        :param radius: radius in pixels
        :param vx: velocity on axis x in pixels per second
        :param vy: velocity on axis y in pixels per second
        """
        self.canvas = canvas
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = vx
        self.vy = vy

        self.alive = True
        self.painting = self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                                fill=color)

    def hit_test(self, obj):
        """
        Function that checks collision between current object and object given in argument.
        :param obj: object to check for collision
        :return: True if there is a collision and False if there is no
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 < (self.radius + obj.radius) ** 2:
            return True
        else:
            return False


class MovingTarget(Ball):
    def __init__(self, canvas, color, x, y, radius, vx, vy):
        """
        Creates Moving Target on Canvas.
        :param canvas: Canvas object
        :param color: target's color in rgb hex, for ex. '#ff0000' is red
        :param x: x coordinate of center in pixels
        :param y: y coordinate of center in pixels
        :param radius: radius in pixels
        :param vx: velocity on axis x in pixels per second
        :param vy: velocity on axis y in pixels per second
        """
        super().__init__(canvas, color, x, y, radius, vx, vy)

    def move(self, dt):
        """
        Updates coordinates after dt time and moves painting on canvas
        to actual coordinates.
        Also checks collisions with canvas borders.
        :param dt: time after last update in seconds
        """
        delta_x = dt * self.vx
        delta_y = dt * self.vy
        self.x += delta_x
        self.y += delta_y

        if self.x < self.radius or self.x > self.canvas.winfo_width() - self.radius:
            self.vx = - self.vx
        if self.y < self.radius or self.y > self.canvas.winfo_height() - self.radius:
            self.vy = - self.vy

        self.canvas.move(self.painting, delta_x, delta_y)


class StaticTarget(MovingTarget):
    def __init__(self, canvas, color, x, y, radius):
        """
        Creates Ball on Canvas.
        :param canvas: Canvas object
        :param color: ball's color in rgb hex, for ex. '#ff0000' is red
        :param x: x coordinate of center in pixels
        :param y: y coordinate of center in pixels
        :param radius: radius in pixels
        """
        super().__init__(canvas, color, x, y, radius, 0, 0)


class Shell(Ball):
    def __init__(self, canvas, color, x, y, radius, vx, vy, g):
        """
        Creates Shell object.
        :param canvas: Canvas object
        :param color: shell's color in rgb hex, for ex. '#ff0000' is red
        :param x: x coordinate of center in pixels
        :param y: y coordinate of center in pixels
        :param radius: radius in pixels
        :param vx: velocity on axis x in pixels per second
        :param vy: velocity on axis y in pixels per second
        :param g: acceleration of gravity
        """
        super().__init__(canvas, color, x, y, radius, vx, vy)
        self.g = g
        self.alive = True

    def move(self, dt):
        """
        Updates coordinates after dt time and moves painting on canvas
        to actual coordinates.
        Also checks collisions with canvas borders.
        :param dt: time after last update in seconds
        """
        delta_x = dt * self.vx
        delta_y = dt * self.vy + self.g * dt**2 / 2
        self.x += delta_x
        self.y += delta_y

        self.vy += self.g * dt

        if self.y > self.canvas.winfo_height() - self.radius:
            self.vy = - self.vy

        self.canvas.move(self.painting, delta_x, delta_y)


class Bomb(Ball):
    def __init__(self, canvas, color, x, y, radius, g):
        super().__init__(canvas, color, x, y, radius, 0, 0)
        self.g = g

    def move(self, dt):
        """
        Updates coordinates after dt time and moves painting on canvas
        to actual coordinates.
        Also checks collisions with canvas borders.
        :param dt: time after last update in seconds
        """
        delta_x = 0
        delta_y = dt * self.vy + self.g * dt**2 / 2
        self.y += delta_y

        self.vy += self.g * dt

        if self.y > self.canvas.winfo_height() - self.radius:
            self.alive = False
            self.canvas.delete(self.painting)

        self.canvas.move(self.painting, delta_x, delta_y)


GameMaster(FPS, WIDTH, HEIGHT, G, TIME_ACCELERATION, POWER, V_MAX, N, TYPES, FILENAME)

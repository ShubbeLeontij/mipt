import tkinter
import random
import json
import time

TIME = 15  # Whole time in seconds
FPS = 144  # Frames per second
N = 5  # Number of targets
WIDTH = 500  # Window width in pixels
HEIGHT = 500  # Window height in pixels
V_MAX = 100  # Max velocity on one axis in pixels per second
RADIUS = 20  # Target radius in pixels
TYPES = ['Triangle', 'Ball']  # Types available for creating
FILENAME = 'leaderboard.json'  # Leaderboard filename


class GameMaster:
    def __init__(self, duration, fps, n, width, height, v_max, radius, types, filename):
        """
        Starts new game
        :param duration: game duration in seconds
        :param fps: frames per second
        :param n: number of targets
        :param width: window width in pixels
        :param height: window height in pixels
        :param v_max: max velocity on one axis in pixels per second
        :param radius: target radius in pixels
        :param types: types available for creating
        :param filename: leaderboard filename (.json)
        """
        self.duration = duration
        self.fps = fps
        self.n = n
        self.width = width
        self.height = height
        self.v_max = v_max
        self.radius = radius
        self.types = types
        self.filename = filename

        self.root = tkinter.Tk()
        self.root.title('Catch the ball')
        self.canvas = tkinter.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack(fill=tkinter.BOTH, expand=1)

        self.name_label = None
        self.name_entry = None
        self.save_button = None
        self.targets = []
        self.score = 0
        self.score_text = self.canvas.create_text(40, 40, text='Score: ' +
                                                               str(self.score))
        self.time_text = self.canvas.create_text(40, 20, text='Time: ' +
                                                              str(round(self.duration, 1)))
        self.init_time = time.time()

        self.main_cycle()
        self.root.mainloop()

    def main_cycle(self):
        """
        Main cycle. Updates all targets and creates new one if necessary.
        Calls itself after (1000 // FPS) ms delay.
        """
        start_time = time.time()
        time_left = self.duration - (start_time - self.init_time)
        self.canvas.itemconfig(self.score_text, text='Score: ' +
                                                     str(self.score))
        self.canvas.itemconfig(self.time_text, text='Time: ' +
                                                    str(round(time_left, 1)))

        for tar in self.targets:  # Update every target
            if tar.dead is False:
                tar.update(1 / self.fps)
            else:
                self.score += tar.dead
                self.targets.remove(tar)

        if len(self.targets) < N:  # Add new target if there are less than N
            self.targets.append(eval(random.choice(self.types) +
                                     '(self.canvas, "#{:06x}".format(random.randint(0, 0xFFFFFF)),'
                                     'random.randint(self.radius, self.width - self.radius),' 
                                     'random.randint(self.radius, self.height - self.radius),'
                                     'random.randint(0, self.v_max), random.randint(0, self.v_max),'
                                     'self.radius)'))

        end_time = time.time()
        if time_left > 0:  # Call main cycle after delay
            wait_time = (1 / self.fps) - (end_time - start_time)
            self.root.after(int(1000 * wait_time) if wait_time > 0 else 1, self.main_cycle)

        else:  # End main cycle
            self.canvas.destroy()

            self.name_label = tkinter.Label(self.root, text='Enter your name:')
            self.name_label.pack()
            self.name_entry = tkinter.Entry(self.root)
            self.name_entry.pack()
            self.save_button = tkinter.Button(self.root, command=self.save_and_show, text='Save')
            self.save_button.pack()

            self.root.bind('<Return>', lambda event: self.save_and_show())

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

        for result in sorted(loaded['results'], key=lambda dic: dic['points'])[::-1]:
            row += 1
            tkinter.Label(self.root, text=result['name']).grid(row=row, column=0)
            tkinter.Label(self.root, text=result['points']).grid(row=row, column=1)


class Target:
    def __init__(self, canvas, painting, x, y, vx, vy, radius, score_prize):
        """
        Creates Target Class object
        :param canvas: Tk.Canvas object where target should be painted
        :param painting: painting id from current canvas
        :param x: x center coordinate in pixels
        :param y: y center coordinate in pixels
        :param vx: velocity on axis x in pixels per second
        :param vy: velocity on axis y in pixels per second
        :param radius: some radius in pixels
        :param score_prize: score prize when target is destroyed
        """
        self.dead = False
        self.canvas = canvas
        self.painting = painting
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.score_prize = score_prize

        self.canvas.tag_bind(self.painting, '<Button-1>', lambda event: self.on_click())

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
        if self.y < self.radius or self.y > self.canvas.winfo_height() - self.radius:
            self.vy = - self.vy

        self.canvas.move(self.painting, delta_x, delta_y)

    def on_click(self):
        """
        Function that changes dead status depending on target type and delete painting on canvas.
        """
        self.dead = self.score_prize
        self.canvas.delete(self.painting)


class Ball(Target):
    def __init__(self, canvas, color, x, y, vx, vy, radius):
        """
        Creates Ball Class object
        :param canvas: Tk.Canvas object where ball should be painted
        :param color: ball color in rgb hex format, for ex. '#ff0000' is red
        :param x: x center coordinate in pixels
        :param y: y center coordinate in pixels
        :param vx: velocity on axis x in pixels per second
        :param vy: velocity on axis y in pixels per second
        :param radius: radius in pixels
        """
        painting = canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                      fill=color, outline='')
        super().__init__(canvas, painting, x, y, vx, vy, radius, 1)

        self.color = color


class Triangle(Target):
    def __init__(self, canvas, color, x, y, vx, vy, max_radius, lifetime=5):
        """
        Creates Triangle Class object
        :param canvas: Tk.Canvas object where triangle should be painted
        :param color: triangle color in rgb hex format, for ex. '#ff0000' is red
        :param x: x center coordinate in pixels
        :param y: y center coordinate in pixels
        :param vx: velocity on axis x in pixels per second
        :param vy: velocity on axis y in pixels per second
        :param max_radius: half of maximum side length in pixels
        :param lifetime: time of triangle`s life in seconds
        """
        painting = canvas.create_polygon((x, y), (x, y), (x, y), fill=color, outline='')
        super().__init__(canvas, painting, x, y, vx, vy, 0, 2)

        self.color = color
        self.max_radius = max_radius
        self.growing_speed = 2 * self.max_radius / lifetime

    def update(self, dt):
        """
        Updates coordinates after dt time and moves painting on canvas to actual coordinates.
        Checks collisions with canvas borders and randomize velocity if there is a collision and
        changes current radius and kills triangle if radius < 0.
        :param dt: time after last update in seconds
        """
        super().update(dt)

        if self.x < self.radius or self.x > self.canvas.winfo_width() - self.radius:
            self.vy = self.vy * random.random() * random.choice([-2, 2])
        if self.y < self.radius or self.y > self.canvas.winfo_height() - self.radius:
            self.vx = self.vx * random.random() * random.choice([-2, 2])

        self.radius += self.growing_speed * dt
        if self.radius > self.max_radius:
            self.growing_speed = -abs(self.growing_speed)
        if self.radius < 0:
            self.dead = 0

        self.canvas.delete(self.painting)
        self.painting = self.canvas.create_polygon((self.x - self.radius, self.y - self.radius),
                                                   (self.x + self.radius, self.y - self.radius),
                                                   (self.x, self.y + self.radius),
                                                   fill=self.color, outline='')
        self.canvas.tag_bind(self.painting, '<Button-1>', lambda event: self.on_click())


GameMaster(TIME, FPS, N, WIDTH, HEIGHT, V_MAX, RADIUS, TYPES, FILENAME)

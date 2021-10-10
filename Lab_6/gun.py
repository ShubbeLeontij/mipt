import random
import tkinter
import math
import time


class Ball:
    def __init__(self, canvas, color, x, y, radius):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.live = True
        self.id = self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius)
        self.canvas.coords(self.id, x - radius, y - radius, x + radius, y + radius)
        self.canvas.itemconfig(self.id, fill=color)


class Shell(Ball):
    def __init__(self, canvas, color, x, y, radius, vx, vy):
        """
        Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        super().__init__(canvas, color, x, y, radius)
        self.vx = vx
        self.vy = vy

    def move(self, dt, g):
        """
        Updates coordinates after dt time and moves painting on canvas to actual coordinates.
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

        self.canvas.move(self.id, delta_x, delta_y)

    def hit_test(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        return True if (self.x - obj.x)**2 + (self.y - obj.y)**2 < (self.radius + obj.radius)**2 else False


class Gun:
    def __init__(self, canvas, color, x, y, length=20, width=10):
        self.canvas = canvas
        self.color = color
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.f2_power = 1
        self.f2_on = False
        self.an = 0
        self.id = self.canvas.create_line(self.x, self.y, self.x + self.length * self.f2_power * math.cos(self.an),
                                          self.y + self.length * self.f2_power * math.sin(self.an), width=self.width)
        self.canvas.bind('<Button-1>', self.fire2_start)
        self.canvas.bind('<ButtonRelease-1>', self.fire2_end)
        self.canvas.bind('<Motion>', self.targeting)

    def fire2_start(self, event):
        self.f2_on = True

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        self.an = math.atan((event.y - self.y) / (event.x - self.x))
        vx = self.f2_power**2 * math.cos(self.an)
        vy = self.f2_power**2 * math.sin(self.an)
        balls += [Shell(self.canvas, '#ff0000', self.x, self.y, 5, vx, vy)]
        self.f2_on = False
        self.f2_power = 1
        self.targeting()

    def targeting(self, event=None):
        """Прицеливание. Зависит от положения мыши."""
        if event and event.x != self.x:
            self.an = math.atan((event.y - self.y) / (event.x - self.x))
        if self.f2_on:
            self.canvas.itemconfig(self.id, fill='orange')
        else:
            self.canvas.itemconfig(self.id, fill='black')
        self.canvas.coords(self.id, self.x, self.y, self.x + math.cos(self.an) * self.length * self.f2_power,
                           self.y + math.sin(self.an) * self.length * self.f2_power)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 5:
                self.f2_power += 0.1
                self.canvas.coords(self.id, self.x, self.y, self.x + math.cos(self.an) * self.length * self.f2_power,
                                   self.y + math.sin(self.an) * self.length * self.f2_power)
            self.canvas.itemconfig(self.id, fill='orange')
        else:
            self.canvas.itemconfig(self.id, fill='black')


def new_game(event=''):
    global screen1, balls, bullet
    bullet = 0
    balls = []
    t1 = Ball(canvas, '#000000', random.randint(0, WIDTH), random.randint(0, HEIGHT), 20)
    g1 = Gun(canvas, '#ff0000', 10, HEIGHT - 10)
    id_points = canvas.create_text(30, 30, text=bullet, font='28')
    while t1.live:
        canvas.itemconfig(id_points, text=bullet)
        for b in balls:
            b.move(10 / FPS, 0.5)
            if b.hit_test(t1) and t1.live:
                t1.live = False
                canvas.delete(id_points)
                canvas.delete(t1.id)
                canvas.itemconfig(screen1, text='Вы уничтожили цель за ' + str(bullet) + ' выстрелов')
        canvas.update()
        time.sleep(1 / FPS)
        g1.power_up()
    time.sleep(5)
    canvas.itemconfig(screen1, text='')
    canvas.delete(g1.id)
    for ball in balls:
        canvas.delete(ball.id)
    new_game()


HEIGHT = 600
WIDTH = 800
FPS = 60

root = tkinter.Tk()
canvas = tkinter.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack(fill=tkinter.BOTH, expand=1)
bullet = 0
balls = []
screen1 = canvas.create_text(400, 300, text='', font='28')

new_game()

root.mainloop()
# TODO Улучшите программу из №1 добавив 2 цели.
# TODO Улучшите программу из №2 сделав цели движущимися.
# TODO Сделать несколько типов снарядов.
# TODO Реализоваль несколько типов целей с различным характером движения.
# TODO Сделать пушку двигающимся танком.
# TODO Создать "бомбочки", которые будут сбрасывать цели на пушку.
# TODO Сделать несколько пушек, которые могут стрелять друг в друга.

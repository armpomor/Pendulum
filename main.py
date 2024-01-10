import pygame as pg
import pymunk
import pymunk.pygame_util
import math
from config import FPS, WIDTH, HEIGHT, COLOR
from body import Ball, Boundary, Line, Structure, Pendulum

# Подгоняем систему координат pymunk к системе координат pygame
pymunk.pygame_util.positive_y_is_up = False

pg.init()


class App:

    def __init__(self, color=COLOR, width=WIDTH, height=HEIGHT, fps=FPS, gravity=(0, 180)):
        self.color = color
        self.width = width
        self.height = height
        self.fps = fps
        self.gravity = gravity

        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption('My Game')
        self.clock = pg.time.Clock()
        self.dt = 1 / self.fps

        self.space = pymunk.Space()  # Пространство
        self.space.gravity = self.gravity  # Гравитация по x и y
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)

        self.ball = None
        self.line = None
        self.pressed_pos = None  # Позиция нажатой кнопки мыши
        self.floor = Boundary()
        self.wall1 = Boundary(x=10, y=self.height / 2, width=25, height=self.height)
        self.wall2 = Boundary(x=self.width - 10, y=self.height / 2, width=25, height=self.height)
        self.ceiling = Boundary(y=10)
        self.add_object()

        self.rect1 = Structure(space=self.space, pos=(1200, self.height - 120), size=(40, 200))
        self.rect2 = Structure(space=self.space, pos=(1500, self.height - 120), size=(40, 200))
        self.rect3 = Structure(space=self.space, pos=(1350, self.height - 240), size=(340, 40))

        self.pendulum = Pendulum(space=self.space)

    @staticmethod
    def calculate_distance(point1, point2):
        return math.dist(point1, point2)

    @staticmethod
    def calculate_angle(point1, point2):
        return math.atan2(point2[1] - point1[1], point2[0] - point1[0])

    def draw(self):
        if self.line and self.pressed_pos:
            pg.draw.line(self.screen, self.line.color, self.pressed_pos, pg.mouse.get_pos(), self.line.width)

        self.space.debug_draw(self.draw_options)
        self.space.step(self.dt)

        pg.display.update()
        self.clock.tick(FPS)
        self.screen.fill(self.color)

    def add_object(self):
        """
        Добавляем новые объекты
        """
        self.space.add(self.floor.body, self.floor.shape)
        self.space.add(self.wall1.body, self.wall1.shape)
        self.space.add(self.wall2.body, self.wall2.shape)
        self.space.add(self.ceiling.body, self.ceiling.shape)

    def run(self):
        while True:
            self.draw()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.ball is None:
                        # Если мяча нет, то создаем его в позиции мыши
                        self.pressed_pos = pg.mouse.get_pos()
                        self.ball = Ball(x=self.pressed_pos[0], y=self.pressed_pos[1])
                        self.line = Line(point1=self.pressed_pos, point2=pg.mouse.get_pos())
                        self.space.add(self.ball.body, self.ball.shape)
                    elif self.pressed_pos:
                        # Если мяч и позиция мыши есть, то прикладываем к нему импульс и делаем мяч динамичным
                        self.ball.body.body_type = pymunk.Body.DYNAMIC
                        angle = self.calculate_angle(self.pressed_pos, pg.mouse.get_pos())
                        force = self.calculate_distance(self.pressed_pos, pg.mouse.get_pos()) * 15
                        fx = math.cos(angle) * force
                        fy = math.sin(angle) * force
                        # self.ball.body.apply_impulse_at_local_point(self.ball.impulse, self.ball.point_impulse)
                        self.ball.body.apply_impulse_at_local_point((fx, fy), self.ball.point_impulse)
                        self.pressed_pos = None
                    else:
                        # Иначе, если мяч есть, а позиции мыши нет, то удаляем мяч из пространства
                        self.space.remove(self.ball.body, self.ball.shape)
                        self.ball = None


if __name__ == '__main__':
    app = App()
    app.run()

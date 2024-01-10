import pymunk
from config import WIDTH, HEIGHT, BROWN


class Ball:
    """
    Класс для динамического объекта
    в виде шара.
    x, y - координаты центра тела
    radius - радиус шара
    mass - масса тела
    color - цвет. Последний аргумент (100) - это непрозрачность, т.е. альфа
    offset — это смещение от центра тяжести тела в локальных координатах тела.
    elasticity - упругость
    friction - трение
    impulse - величина импульса прикладываемого к шару
    point_impulse - точка, к которой прикладывается импульс. Если (0, 0), то к центру
    """

    def __init__(self, x=300, y=50, radius=30, mass=20, color=(0, 255, 0, 100), offset=(0, 0), elasticity=0.9,
                 friction=1.4, impulse=(10, -100), point_impulse=(0, 0)):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.color = color
        self.offset = offset
        self.elasticity = elasticity
        self.friction = friction
        self.impulse = impulse
        self.point_impulse = point_impulse
        self.body.position = (self.x, self.y)
        self.shape = pymunk.Circle(self.body, self.radius, self.offset)
        self.shape.mass = self.mass
        self.shape.color = self.color
        self.shape.elasticity = self.elasticity
        self.shape.friction = self.friction


class Boundary:
    """
    Класс для статических объектов.
    x, y - координаты центра объекта
    width - ширина
    height - высота
    elasticity - упругость
    friction - трение
    """

    def __init__(self, x=WIDTH / 2, y=HEIGHT, width=WIDTH, height=25, color=(0, 0, 255, 100), elasticity=0.4,
                 friction=0.5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.elasticity = elasticity
        self.friction = friction
        self.size = (self.width, self.height)
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (self.x, self.y)
        self.shape = pymunk.Poly.create_box(self.body, self.size)
        self.shape.color = self.color
        self.shape.elasticity = self.elasticity
        self.shape.friction = self.friction


class Line:
    """
    Класс для линий.
    """

    def __init__(self, point1=(0, 0), point2=(0, 0), color='white', width=3):
        self.point1 = point1
        self.point2 = point2
        self.color = color
        self.width = width


class Structure:
    """
    Класс для блоков (прямоугольников).
    """

    def __init__(self, space, pos=(0, 0), size=(10, 10), color=BROWN, mass=100, radius=2):
        self.space = space
        self.pos = pos
        self.size = size
        self.color = color
        self.mass = mass
        self.radius = radius

        self.body = pymunk.Body()
        self.body.position = self.pos
        self.shape = pymunk.Poly.create_box(self.body, self.size, self.radius)
        self.shape.color = self.color
        self.shape.mass = self.mass
        self.shape.elasticity = 0.4
        self.shape.friction = 0.4

        self.space.add(self.body, self.shape)


class Pendulum:
    """
    Маятник
    rotation_body_center - ось маятника
    pos_center - позиция центра маятника
    body - тело маятника
    pos_body - позиция тела маятника
    line - шарнир маятника (тело, начальная точка относительно тела, конечная точка относительно тела, толщина)
    circle - отвес маятника (тело, радиус отвеса, центр отвеса относительно тела)
    rotation_center_join - соединение маятника
    radius - радиус отвеса маятника
    point1_line - начальная точка шарнира маятника относительно тела
    point2_line - конечная точка шарнира маятника относительно тела
    width_line - толщина шарнира маятника
    pos_circle - координаты центра отвеса маятника относительно тела
    """

    def __init__(self, space, pos_center=(850, 500), pos_body=(850, 600), friction_line=1, friction_circle=1,
                 mass_line=8, mass_circle=30, elasticity_line=0.1, elasticity_circle=0.95, radius=40,
                 color_circle=(111, 0, 111, 100), point1_line=(0, 0), point2_line=(325, 0), width_line=3,
                 pos_circle=(325, 0)):
        self.space = space
        self.pos_center = pos_center
        self.pos_body = pos_body
        self.friction_line = friction_line
        self.friction_circle = friction_circle
        self.mass_line = mass_line
        self.mass_circle = mass_circle
        self.elasticity_line = elasticity_line
        self.elasticity_circle = elasticity_circle
        self.radius = radius
        self.color_circle = color_circle
        self.point1_line = point1_line
        self.point2_line = point2_line
        self.width_line = width_line
        self.pos_circle = pos_circle

        self.rotation_body_center = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.rotation_body_center.position = self.pos_center

        self.body = pymunk.Body()
        self.body.position = self.pos_body

        self.line = pymunk.Segment(self.body, self.point1_line, self.point2_line, self.width_line)
        self.circle = pymunk.Circle(self.body, self.radius, self.pos_circle)

        self.line.friction = self.friction_line
        self.circle.friction = self.friction_circle
        self.line.mass = self.mass_line
        self.circle.mass = self.mass_circle
        self.circle.color = self.color_circle
        self.line.elasticity = self.elasticity_line
        self.circle.elasticity = self.elasticity_circle

        # Собираем маятник
        self.rotation_center_join = pymunk.PinJoint(self.body, self.rotation_body_center, (0, 0), (0, 0))
        # Добавляем в пространство
        self.space.add(self.body, self.line, self.circle, self.rotation_center_join)

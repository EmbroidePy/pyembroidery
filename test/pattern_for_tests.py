from pyembroidery import *

import math


def evaluate_lsystem(symbol, rules, depth):
    if depth <= 0 or symbol not in rules:
        symbol()
    else:
        for produced_symbol in rules[symbol]:
            evaluate_lsystem(produced_symbol, rules, depth - 1)


class Turtle:
    def __init__(self, pattern):
        self.pattern = pattern
        self.angle = 0
        self.x = 0
        self.y = 0
        import math
        self.turn_amount = math.pi / 3

    def forward(self, distance):
        self.x += distance * math.cos(self.angle)
        self.y += distance * math.sin(self.angle)
        self.pattern.add_stitch_absolute(STITCH, self.x, self.y)
        # self.pattern.add_stitch_absolute(SEQUIN_EJECT, self.x, self.y)

    def turn(self, angle):
        self.angle += angle

    def move(self, distance):
        self.x += distance * math.cos(self.angle)
        self.y += distance * math.sin(self.angle)

    def add_gosper(self):
        a = lambda: self.forward(20)
        b = lambda: self.forward(20)
        l = lambda: self.turn(self.turn_amount)
        r = lambda: self.turn(-self.turn_amount)
        initial = lambda: None
        rules = {
            initial: [a],
            a: [a, l, b, l, l, b, r, a, r, r, a, a, r, b, l],
            b: [r, a, l, b, b, l, l, b, l, a, r, r, a, r, b]
        }
        evaluate_lsystem(initial, rules, 3)  # 4

    def add_serp(self):
        a = lambda: self.forward(20)
        b = lambda: self.forward(20)
        l = lambda: self.turn(self.turn_amount)
        r = lambda: self.turn(-self.turn_amount)
        initial = lambda: None
        rules = {
            initial: [a],
            a: [b, l, a, l, b],
            b: [a, r, b, r, a]
        }
        evaluate_lsystem(initial, rules, 3)  # 6

def get_big_pattern():
    pattern = EmbPattern()
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "red")
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "blue")
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "green")
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "grey")
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "gold")
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "ivory")
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "khaki")
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "oldlace")
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "olive")
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "pink")
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "purple")
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "tan")
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "violet")
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "white")
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "salmon")
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "lime")  # 16 blocks.
    return pattern


def get_shift_pattern():
    pattern = EmbPattern()
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "red")
    pattern.add_command(MATRIX_TRANSLATE, 25, 25)
    pattern.add_command(MATRIX_ROTATE, 22.5)
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "blue")
    pattern.add_command(MATRIX_TRANSLATE, 25, 25)
    pattern.add_command(MATRIX_ROTATE, 22.5)
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "green")
    pattern.add_command(MATRIX_TRANSLATE, 25, 25)
    pattern.add_command(MATRIX_ROTATE, 22.5)
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "grey")
    pattern.add_command(MATRIX_TRANSLATE, 25, 25)
    pattern.add_command(MATRIX_ROTATE, 22.5)
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "gold")
    pattern.add_command(MATRIX_TRANSLATE, 25, 25)
    pattern.add_command(MATRIX_ROTATE, 22.5)
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "ivory")
    pattern.add_command(MATRIX_TRANSLATE, 25, 25)
    pattern.add_command(MATRIX_ROTATE, 22.5)
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "khaki")
    pattern.add_command(MATRIX_TRANSLATE, 25, 25)
    pattern.add_command(MATRIX_ROTATE, 22.5)
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "oldlace")
    pattern.add_command(MATRIX_TRANSLATE, 25, 25)
    pattern.add_command(MATRIX_ROTATE, 22.5)
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "olive")
    pattern.add_command(MATRIX_TRANSLATE, 25, 25)
    pattern.add_command(MATRIX_ROTATE, 22.5)
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "pink")
    pattern.add_command(MATRIX_TRANSLATE, 25, 25)
    pattern.add_command(MATRIX_ROTATE, 22.5)
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "purple")
    pattern.add_command(MATRIX_TRANSLATE, 25, 25)
    pattern.add_command(MATRIX_ROTATE, 22.5)
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "tan")
    pattern.add_command(MATRIX_TRANSLATE, 25, 25)
    pattern.add_command(MATRIX_ROTATE, 22.5)
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "violet")
    pattern.add_command(MATRIX_TRANSLATE, 25, 25)
    pattern.add_command(MATRIX_ROTATE, 22.5)
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "white")
    pattern.add_command(MATRIX_TRANSLATE, 25, 25)
    pattern.add_command(MATRIX_ROTATE, 22.5)
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "salmon")
    pattern.add_command(MATRIX_TRANSLATE, 25, 25)
    pattern.add_command(MATRIX_ROTATE, 22.5)
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "lime")
    return pattern


def get_simple_pattern():
    pattern = EmbPattern()
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "red")
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "blue")
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "green")
    return pattern


def get_random_pattern_large(count=1000):
    pattern = EmbPattern()
    import random

    for i in range(0, count):
        pattern.add_block(
            [(random.uniform(-500, 500), random.uniform(-500, 500)),
             (random.uniform(-500, 500), random.uniform(-500, 500)),
             (random.uniform(-500, 500), random.uniform(-500, 500))],
            random.randint(0x000000, 0xFFFFFF))
    return pattern


def get_random_pattern_small():
    pattern = EmbPattern()
    import random

    pattern.add_block(
        [(random.uniform(-500, 500), random.uniform(-500, 500)),
         (random.uniform(-500, 500), random.uniform(-500, 500)),
         (random.uniform(-500, 500), random.uniform(-500, 500))],
        random.randint(0x000000, 0xFFFFFF))
    return pattern


def get_random_pattern_small_halfs():
    pattern = EmbPattern()
    import random
    pattern.add_block(
        [(random.randint(-500, 500) / 2.0, random.randint(-500, 500) / 2.0),
         (random.randint(-500, 500) / 2.0, random.randint(-500, 500) / 2.0),
         (random.randint(-500, 500) / 2.0, random.randint(-500, 500) / 2.0)],
        random.randint(0x000000, 0xFFFFFF))
    return pattern


def get_fractal_pattern():
    pattern = EmbPattern()
    turtle = Turtle(pattern)
    turtle.add_gosper()
    pattern.add_command(COLOR_BREAK)
    turtle.move(500)
    turtle.add_serp()
    pattern.add_command(SEQUENCE_BREAK)
    pattern.add_command(STOP)
    turtle.move(50)
    turtle.add_serp()
    pattern.add_command(SEQUENCE_BREAK)
    turtle.turn(-math.pi / 3)
    turtle.move(500)
    turtle.add_serp()
    pattern.add_command(COLOR_BREAK)
    turtle.turn(-math.pi / 3)
    turtle.move(500)  # 260, -450
    turtle.add_gosper()
    pattern.add_command(END)
    return pattern

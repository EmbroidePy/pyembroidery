from pyembroidery import *


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
    pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "lime")
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


def get_random_pattern_large():
    pattern = EmbPattern()
    import random

    for i in range(0, 1000):
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

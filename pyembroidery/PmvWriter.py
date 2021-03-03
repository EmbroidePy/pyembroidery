from .EmbConstant import *
from .WriteHelper import write_int_8, write_int_16le, write_string_utf8

MAX_STITCH_DISTANCE = 70
MAX_PERMITTED_STITCHES = 100


def write(pattern, f, settings=None):
    max_x = -200000000
    min_x = +200000000
    max_y = -200000000
    min_y = +200000000
    point_count = 0
    for stitch in pattern.stitches:
        data = stitch[2]
        x = stitch[0]
        y = -stitch[1]
        if data == STITCH or data == JUMP:
            point_count += 1
            if x > max_x:
                max_x = x
            if x < min_x:
                min_x = x
            if y > max_y:
                max_y = y
            if y < min_y:
                min_y = y
        if point_count >= MAX_PERMITTED_STITCHES:
            break
    center_y = (min_y + max_y) / 2.0
    normal_max_y = max_y - center_y
    if normal_max_y > 35.0:  # 14 * 2.5 = 35.0
        scale_y = 14.0 / normal_max_y  # 1 / (normal_max_y / 14.0)
    else:
        scale_y = 1.0 / 2.5  # pure unit conversion.
    scale_x = 1.0 / 2.5

    write_string_utf8(f, "#PMV0001")
    header = "...................................."
    write_string_utf8(f, header[0:36])
    f.write(
        b"\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00"
    )

    write_int_16le(f, point_count)
    write_int_16le(f, point_count * 2)
    point_index = -1
    max_x = -200000000
    min_x = +200000000
    max_y = -200000000
    min_y = +200000000
    xx = 0
    for stitch in pattern.stitches:
        point_index += 1
        if point_index >= point_count:
            break
        data = stitch[2] & COMMAND_MASK
        x = stitch[0]
        y = -stitch[1]
        x *= scale_x
        y -= center_y
        y *= scale_y
        y = int(round(y))
        x = int(round(x - xx))
        xx += x
        if data == STITCH or data == JUMP:
            if xx > max_x:
                max_x = xx
            if xx < min_x:
                min_x = xx
            if y > max_y:
                max_y = y
            if y < min_y:
                min_y = y

            if x < 0:
                x += 64
            if y < 0:
                y += 32
            write_int_8(f, x)
            write_int_8(f, y)
            continue
    write_int_16le(f, 0)
    write_int_16le(f, 256)
    f.write(b"\x00\x00\x00\x00\x05\x00\x00\x00" b"\x00\x00\x00\x00\x00\x00\x02\x00")
    write_int_16le(f, 256)
    write_int_8(f, 0)
    write_int_8(f, 0)
    length_range = max_x - min_x
    write_length_lookup_table(f, length_range)
    width_range = max_y - min_y
    write_width_lookup_table(f, width_range)
    write_int_16le(f, 0x12)
    f.write(b"\x00\x00\x00\x00\x00\x00\x00\x00" b"\x00\x00\x00\x00\x00\x00\x00\x00")


def write_length_lookup_table(f, length_range):
    # I've not solved this for how they are actually made, writing a something that should work.
    write_values = [
        (0, 0),
        (10, 71),
        (20, 143),
        (40, 214),
        (60, 286),
        (80, 357),
        (100, 429),
        (120, 500),
        (140, 571),
        (160, 714),
        (180, 786),
        (200, 857),
        (250, 1000),
        (300, 1286),
        (350, 1429),
        (400, 1571),
        (450, 1786),
        (500, 2000),
    ]

    steps = len(write_values)
    write_int_8(f, steps - 1)  # (500, 2000)
    write_int_8(f, steps)
    for value in write_values:
        length_at_step = value[0]
        other_at_step = value[1]
        write_int_16le(f, length_at_step)
        write_int_16le(f, other_at_step)


def write_width_lookup_table(f, width_range):
    if width_range == 0:
        write_int_8(f, 0)
        write_int_8(f, 1)
        write_int_16le(f, 8192)
        write_int_16le(f, 1000)
        return
    steps = 15
    second_max = 28000.0 / float(width_range)
    second_step = second_max / float(steps - 1)
    write_int_8(f, steps - 1)
    write_int_8(f, steps)
    for i in range(0, steps):
        width_at_step = 50 * i
        other_at_step = second_step * i

        write_int_16le(f, width_at_step)
        write_int_16le(f, int(round(other_at_step)))

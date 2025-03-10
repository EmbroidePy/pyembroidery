from .EmbConstant import *
from .WriteHelper import write_int_8, write_int_16le, write_int_32le

FULL_JUMP = False
ROUND = True
MAX_JUMP_DISTANCE = 124  # 0xFCFF/2 16 bit signed, FD,FE,FF reserved.
MAX_STITCH_DISTANCE = 124


def write_xxx_header_b(pattern, f):
    stitches = pattern.stitches
    for i in range(0, 0x17):
        write_int_8(f, 0x00)
    write_int_32le(f, len(stitches) - 1)
    # END command not called a command.
    for i in range(0, 0x0C):
        write_int_8(f, 0x00)
    write_int_32le(f, len(pattern.threadlist))
    write_int_16le(f, 0x0000)

    extends = pattern.bounds()
    width = int(extends[2] - extends[0])
    height = int(extends[3] - extends[1])
    write_int_16le(f, width)
    write_int_16le(f, height)
    write_int_16le(f, int(stitches[-1][0]))
    write_int_16le(f, int(-stitches[-1][1]))
    write_int_16le(f, int(-extends[0]))
    write_int_16le(f, int(extends[3]))
    for i in range(0, 0x42):
        write_int_8(f, 0x00)
    write_int_16le(f, 0x00)  # unknown
    write_int_16le(f, 0x00)  # unknown
    for i in range(0, 0x73):
        write_int_8(f, 0x00)
    write_int_16le(f, 0x20)
    for i in range(0, 0x08):
        write_int_8(f, 0x00)


def write_xxx_header_a(pattern, f):
    stitches = pattern.stitches
    for i in range(0, 0x17):
        write_int_8(f, 0x00)
    write_int_32le(f, len(stitches) - 1)
    # END command not called a command.
    for i in range(0, 0x0C):
        write_int_8(f, 0x00)
    write_int_32le(f, len(pattern.threadlist))
    write_int_16le(f, 0x0000)

    write_int_16le(f, int(stitches[-1][0]))  # correct
    write_int_16le(f, int(-stitches[-1][1]))  # correct
    for i in range(0, 0x85):
        write_int_8(f, 0x00)
    f.write(b"XXX")
    for i in range(0, 0x39):
        write_int_8(f, 0x00)
    write_int_16le(f, 0x20)
    for i in range(0, 0x08):
        write_int_8(f, 0x00)


def write_xxx_stitches(pattern, f):
    stitches = pattern.stitches
    xx = 0
    yy = 0
    for stitch in stitches:
        x = stitch[0]
        y = stitch[1]
        data = stitch[2] & COMMAND_MASK
        dx = int(round(x - xx))
        dy = int(round(y - yy))
        xx += dx
        yy += dy
        if data == COLOR_CHANGE or data == STOP:
            write_int_8(f, 0x7F)
            write_int_8(f, 0x08)
            write_int_8(f, dx)
            write_int_8(f, -dy)
            continue
        if data == END:
            break
        if data == STITCH:
            if -124 < dx < 124 and -124 < dy < 124:
                write_int_8(f, dx)
                write_int_8(f, -dy)
                continue
            else:
                write_int_8(f, 0x7D)
                write_int_16le(f, dx)
                write_int_16le(f, -dy)
                continue
        if data == TRIM:
            write_int_8(f, 0x7F)
            write_int_8(f, 0x03)
            write_int_8(f, dx)
            write_int_8(f, -dy)
            continue
        if data == JUMP:
            write_int_8(f, 0x7F)
            write_int_8(f, 0x01)
            write_int_8(f, dx)
            write_int_8(f, -dy)
            continue


def write_xxx_colors(pattern, f):
    write_int_8(f, 0x00)
    write_int_8(f, 0x00)
    current_color = 0
    colors = pattern.threadlist
    for color in colors:
        write_int_8(f, 0x00)
        write_int_8(f, color.get_red())
        write_int_8(f, color.get_green())
        write_int_8(f, color.get_blue())
        current_color += 1
    for i in range(0, 21 - current_color):
        write_int_32le(f, 0x00000000)
    write_int_32le(f, 0xFFFFFF00)
    write_int_8(f, 0x00)
    write_int_8(f, 0x01)


def write(pattern, f, settings=None):
    write_xxx_header_b(pattern, f)
    place_holder_for_end_of_stitches = f.tell()
    write_int_32le(f, 0x00000000)
    write_xxx_stitches(pattern, f)
    end_of_stitches = f.tell()
    f.seek(place_holder_for_end_of_stitches, 0)
    write_int_32le(f, end_of_stitches)
    f.seek(end_of_stitches, 0)
    write_int_8(f, 0x7F)
    write_int_8(f, 0x7F)
    write_int_8(f, 0x02)
    write_int_8(f, 0x14)
    write_xxx_colors(pattern, f)

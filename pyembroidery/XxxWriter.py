from .EmbConstant import *
from .WriteHelper import write_int_8, write_int_16le, write_int_32le

FULL_JUMP = False
ROUND = True
MAX_JUMP_DISTANCE = 0x7E7F  # 0xFCFF/2 16 bit signed, FD,FE,FF reserved.
MAX_STITCH_DISTANCE = 124


def write(pattern, f, settings=None):
    stitches = pattern.stitches
    current_color = 0
    if len(stitches) != 0:
        xx = stitches[0][0]
        yy = stitches[0][1]
    else:
        xx = 0
        yy = 0
    for i in range(0, 0x17):
        write_int_8(f, 0x00)
    write_int_32le(f, len(stitches) - 1)
    # END command not called a command.
    for i in range(0, 0x0C):
        write_int_8(f, 0x00)
    write_int_16le(f, len(pattern.threadlist))
    write_int_16le(f, 0x0000)
    write_int_16le(f, 0x0000)

    extends = pattern.bounds()
    width = int(extends[2] - extends[0])
    height = int(extends[3] - extends[1])
    write_int_16le(f, width)
    write_int_16le(f, height)
    half_width = int(width / 2)
    half_height = int(height / 2)
    write_int_16le(f, int(stitches[-1][0]))  # correct
    write_int_16le(f, int(-stitches[-1][1]))  # correct
    write_int_16le(f, int(half_width))  # wrong
    write_int_16le(f, int(half_height))  # wrong
    for i in range(0, 0xC5):
        write_int_8(f, 0x00)
    place_holder_for_end_of_stitches = f.tell()
    write_int_16le(f, 0x0000)

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
            write_int_8(f, 0x7F)
            write_int_8(f, 0x7F)
            break
        if data == JUMP:
            if -124 < dx < 124 and -124 < dy < 124:
                write_int_8(f, 0x7F)
                write_int_8(f, 0x01)
                write_int_8(f, dx)
                write_int_8(f, -dy)
                continue
            else:
                write_int_8(f, 0x7D)
                write_int_16le(f, dx)
                write_int_16le(f, -dy)
                continue
        if data == STITCH:
            write_int_8(f, dx)
            write_int_8(f, -dy)
            continue
    end_of_stitches = f.tell()
    f.seek(place_holder_for_end_of_stitches, 0)
    write_int_16le(f, end_of_stitches)
    f.seek(end_of_stitches, 0)
    write_int_8(f, 0x02)
    write_int_8(f, 0x14)
    write_int_8(f, 0x00)
    write_int_8(f, 0x00)
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

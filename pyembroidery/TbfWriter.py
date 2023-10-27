from . import decode_embroidery_command
from .EmbConstant import *
from .WriteHelper import write_string_utf8, write_int_8

FULL_JUMP = False
ROUND = True
MAX_JUMP_DISTANCE = 127
MAX_STITCH_DISTANCE = 127
THREAD_CHANGE_COMMAND = NEEDLE_SET


def write(pattern, f, settings=None):
    bounds = pattern.bounds()

    name = pattern.get_metadata("name", "Untitled")
    write_string_utf8(f, "3.00")
    for i in range(f.tell(), 0x80):
        f.write(b"\x20")  # space
    write_string_utf8(f, "LA:%-16s\r" % name)
    write_string_utf8(f, "ST:%7d\r" % pattern.count_stitches())
    write_string_utf8(f, "CO:%3d\r" % pattern.count_color_changes())

    write_string_utf8(f, "+X:%5d\r" % abs(bounds[2]))
    write_string_utf8(f, "-X:%5d\r" % abs(bounds[0]))
    write_string_utf8(f, "+Y:%5d\r" % abs(bounds[3]))
    write_string_utf8(f, "-Y:%5d\r" % abs(bounds[1]))
    ax = 0
    ay = 0
    if len(pattern.stitches) > 0:
        last = len(pattern.stitches) - 1
        ax = int(pattern.stitches[last][0])
        ay = -int(pattern.stitches[last][1])
    if ax >= 0:
        write_string_utf8(f, "AX:+%5d\r" % ax)
    else:
        write_string_utf8(f, "AX:-%5d\r" % abs(ax))
    if ay >= 0:
        write_string_utf8(f, "AY:+%5d\r" % ay)
    else:
        write_string_utf8(f, "AY:-%5d\r" % abs(ay))

    # TP is unknown.
    tp = pattern.get_metadata("tp", "EG/")
    write_string_utf8(f, "TP:%-32s\r" % tp)

    # JC is unknown.
    jc = "3"
    write_string_utf8(f, "JC:%s\r" % jc)

    # DO is the thread order.
    write_string_utf8(f, "DO:")
    thread_order = [0] * 0x100
    index = 0
    for stitch in pattern.stitches:
        data = stitch[2] & COMMAND_MASK
        if data == NEEDLE_SET:
            flag, thread, needle, order = decode_embroidery_command(stitch[2])
            thread_order[index] = needle
            index += 1
    for n in thread_order:
        write_int_8(f, n)
    write_string_utf8(f, "\r")

    # DA is the threadlist. This is not *only* the used threads but any threads in the set.
    write_string_utf8(f, "DA:")
    if len(pattern.threadlist) > 0:
        for thread in pattern.threadlist:
            write_int_8(f, 0x45)
            write_int_8(f, thread.get_red())
            write_int_8(f, thread.get_green())
            write_int_8(f, thread.get_blue())
            write_int_8(f, 0x20)

    # Padding to 501
    for i in range(f.tell(), 0x501):
        f.write(b"\x20")  # space

    # Seen in only some files.
    f.write(b"\x0d\x1A")

    # Pad to the end of the header.
    for i in range(f.tell(), 0x600):
        f.write(b"\x20")  # space
    # END HEADER

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

        if data == STITCH:
            cmd = 0x80
            f.write(bytes(bytearray([dx & 0xFF, dy & 0xFF, cmd])))
        elif data == JUMP:
            cmd = 0x90
            f.write(bytes(bytearray([dx & 0xFF, dy & 0xFF, cmd])))
        elif data == STOP:
            cmd = 0x40
            f.write(bytes(bytearray([dx & 0xFF, dy & 0xFF, cmd])))
        elif data == TRIM:
            cmd = 0x86
            f.write(bytes(bytearray([dx & 0xFF, dy & 0xFF, cmd])))
        elif data == NEEDLE_SET:
            cmd = 0x81
            f.write(bytes(bytearray([dx & 0xFF, dy & 0xFF, cmd])))
        elif data == END:
            cmd = 0x8F
            f.write(bytes(bytearray([dx & 0xFF, dy & 0xFF, cmd])))
            break
    # Terminal character.
    f.write(b"\x1a")

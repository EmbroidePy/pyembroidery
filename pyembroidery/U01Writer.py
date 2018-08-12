from .EmbConstant import *
from .WriteHelper import write_int_16le, write_int_32le

SEQUIN_CONTINGENCY = CONTINGENCY_SEQUIN_JUMP
STRIP_SPEEDS = False
FULL_JUMP = False
MAX_JUMP_DISTANCE = 127
MAX_STITCH_DISTANCE = 127


def write(pattern, f, settings=None):
    stitches = pattern.stitches
    stitch_count = len(stitches)
    for i in range(0, 0x80):
        f.write(b'0')
    if stitch_count == 0:
        return
    extends = pattern.extends()
    write_int_16le(f, int(extends[0]))
    write_int_16le(f, -int(extends[3]))
    write_int_16le(f, int(extends[2]))
    write_int_16le(f, -int(extends[1]))
    write_int_32le(f, 0)  # Dunno.

    write_int_32le(f, stitch_count + 1)  # force write first needle position
    last_stitch = stitches[stitch_count - 1]
    write_int_16le(f, int(last_stitch[0]))
    write_int_16le(f, -int(last_stitch[1]))
    for i in range(f.tell(), 0x100):
        f.write(b'\x00')
    xx = 0
    yy = 0
    needle = 1
    f.write(b'\xE9\x00\x00')  # Needle to C1
    trigger_fast = False
    trigger_slow = False
    for stitch in stitches:
        x = stitch[0]
        y = stitch[1]
        data = stitch[2]
        dx = int(round(x - xx))
        dy = int(round(y - yy))
        xx += dx
        yy += dy
        if data == SLOW:
            trigger_slow = True
            continue
        if data == FAST:
            trigger_fast = True
            continue
        cmd = 0x80
        if dy >= 0:
            cmd |= 0x40
        if dx <= 0:
            cmd |= 0x20
        delta_x = abs(dx)
        delta_y = abs(dy)
        if data == STITCH:
            if trigger_fast:
                trigger_fast = False
                cmd |= 0x02
            if trigger_slow:
                trigger_slow = False
                cmd |= 0x04
            f.write(bytes(bytearray([cmd, delta_y, delta_x])))
        elif data == JUMP:  # If you did both FAST, SLOW, and JUMP, you'd get a trim.
            if trigger_fast:
                trigger_fast = False
                cmd |= 0x02
            if trigger_slow:
                trigger_slow = False
                cmd |= 0x04
            cmd |= 0x01
            f.write(bytes(bytearray([cmd, delta_y, delta_x])))
        elif data == STOP:
            cmd |= 0x08
            f.write(bytes(bytearray([cmd, delta_y, delta_x])))
        elif data == TRIM:
            cmd |= 0x07
            f.write(bytes(bytearray([cmd, delta_y, delta_x])))
        elif data == COLOR_CHANGE:
            needle %= 7
            needle += 1
            cmd = cmd + 8 + needle
            f.write(bytes(bytearray([cmd, delta_y, delta_x])))
        elif data == END:
            f.write(b'\xF8\x00\x00')
            break

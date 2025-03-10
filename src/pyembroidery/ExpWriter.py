from .EmbConstant import *

SEQUIN_CONTINGENCY = CONTINGENCY_SEQUIN_JUMP
FULL_JUMP = True
ROUND = True
MAX_JUMP_DISTANCE = 127
MAX_STITCH_DISTANCE = 127


def write(pattern, f, settings=None):
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
            # consider bounds checking the delta_x, delta_y and raising ValueError if exceeds.
            delta_x = dx & 0xFF
            delta_y = -dy & 0xFF
            f.write(bytes(bytearray([delta_x, delta_y])))
        elif data == JUMP:
            delta_x = dx & 0xFF
            delta_y = -dy & 0xFF
            f.write(b"\x80\x04")
            f.write(bytes(bytearray([delta_x, delta_y])))
        elif data == TRIM:
            f.write(b"\x80\x80\x07\x00")
            continue
        elif data == COLOR_CHANGE:
            f.write(b"\x80\x01\x00\x00")
            continue
        elif data == STOP:
            f.write(b"\x80\x01\x00\x00")
            continue
        elif data == END:
            pass

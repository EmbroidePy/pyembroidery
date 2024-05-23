"""
HPGL2 Plot vector graphics are used commonly in pen plotters and vinyl cutters and have been a pretty mature language
since the 1970s. Here we are using a subset of the main language and commands to work with somewhat common form of
quilting machine. While this will process a lot of the more complex methods simple quilting stitches are expected to
work and are the typical goal product.

The standard step size of 1 unit in HPGL is 1/40 mm. As opposed to 1/10 mm which is standard for embroidery. HPGL is
increasing Y is downwards, which is contrary to most embroidery.
"""

from .WriteHelper import write_string_utf8

from .EmbFunctions import *


def write(pattern, f, settings=None):
    write_string_utf8(f, "IN;")
    write_string_utf8(f, "IP;")

    trimmed = True

    stitches = pattern.stitches
    xx = 0
    yy = 0

    pen_id = 1
    write_string_utf8(f, "SP%d;" % pen_id)

    for stitch in stitches:
        # 4 to convert 1/10mm to 1/40mm.
        x = stitch[0] * 4.0
        y = stitch[1] * 4.0
        data = stitch[2] & COMMAND_MASK
        dx = int(round(x - xx))
        dy = int(round(y - yy))
        xx += dx
        yy += dy
        if data == STITCH:
            write_string_utf8(f, "PD %d, %d;" % (int(xx), int(yy)))
            trimmed = False
        elif data == JUMP:
            if trimmed:
                write_string_utf8(f, "PU %d, %d;" % (int(xx), int(yy)))
            else:
                write_string_utf8(f, "PD %d, %d;" % (int(xx), int(yy)))
        elif data == COLOR_CHANGE:
            pen_id += 1
            write_string_utf8(f, "SP%d;" % pen_id)
            trimmed = True
        elif data == STOP:
            trimmed = True
        elif data == TRIM:
            trimmed = True
        elif data == END:
            write_string_utf8(f, "EN;")
            break

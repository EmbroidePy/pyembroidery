from .EmbThread import EmbThread
from .ReadHelper import read_int_8, read_int_16le, read_int_32be, signed8, signed16

# 7F 08 00 00 is color change.
# 7F 01 xx yy is unstitched.
# 7F 7F 02 14 is end.


def read(f, out, settings=None):
    f.seek(0x27, 1)
    num_of_colors = read_int_16le(f)
    f.seek(0x100, 0)
    while True:
        b1 = read_int_8(f)
        if b1 == 0x7D or b1 == 0x7E:  # not seen a 7E big jump code
            x = read_int_16le(f)
            y = read_int_16le(f)
            out.move(signed16(x), -signed16(y))
            continue
        b2 = read_int_8(f)
        if b1 != 0x7F:
            out.stitch(signed8(b1), -signed8(b2))
            continue
        b3 = read_int_8(f)
        b4 = read_int_8(f)
        if b2 == 0x01:
            out.move(signed8(b3), -signed8(b4))
            continue
        elif b2 == 0x03:
            out.trim()
            x = signed8(b3)
            y = -signed8(b4)
            if x != 0 or y != 0:
                out.move(x, y)
            continue
        elif b2 == 0x08 or 0x0A <= b2 <= 0x17:
            out.color_change()
            continue
        elif b2 == 0x7F:
            break  # End
        elif b2 == 0x18:
            break  # End
    out.end()
    f.seek(2, 1)
    for i in range(0, num_of_colors):
        thread = EmbThread()
        thread.color = read_int_32be(f)
        if thread.color is None:
            break
        else:
            out.add_thread(thread)

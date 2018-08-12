from .ReadHelper import read_int_16le, read_int_8, read_int_32be, signed8, signed16
from .EmbThread import EmbThread


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
        if b1 == 0x7F:
            b3 = read_int_8(f)
            b4 = read_int_8(f)
            if b2 == 0x01:
                out.move(signed8(b3), -signed8(b4))
                continue
            elif b2 == 0x08:
                out.color_change()
                continue
            if b2 == 0x7F:
                out.end(0)
                break
            else:
                pass
        else:
            out.stitch(signed8(b1), -signed8(b2))
    out.end()
    f.seek(2, 1)
    for i in range(0, num_of_colors + 1):
        thread = EmbThread()
        thread.color = read_int_32be(f)
        if thread.color is None:
            break
        else:
            out.add_thread(thread)
